<?php
/**
 *   Differential Diagnose Support System
 *   Copyright (C) 2023  ddss.software@gmail.com

 *   This program is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program.  If not, see <https://www.gnu.org/licenses/>
 */
namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Symfony\Component\Finder\Finder;
use Symfony\Component\Yaml\Yaml;
use Illuminate\Support\Arr;

class LoadBiblioCommand extends Command
{
    protected $signature = 'biblio:load';

    protected $description = 'Loads biblio file into database';

    public $locale;
    public $biblioPath;

    public function __construct()
    {
        parent::__construct();
        $this->finder = new Finder();
    }

    public function handle()
    {
        $this->info('Started loading biblio');

        $this->loadLocale();
        $this->clearData();
        $this->loadTests();
        $this->loadSymptoms();
        $this->loadConditions();
        $this->fillData();
        $this->loadSuggestionsTable();

        $this->info('Ended loading biblio');

        return Command::SUCCESS;
    }

    public function clearData()
    {
        $this->info('Clearing data');
        $tables = [
            'conditions',
            'symptoms',
            'tests',
            'condition_symptom',
            'symptom_test',
            'conditionsaka',
            'symptomsaka',
            'suggestions',
        ];
        $tables = array_reverse($tables);
        foreach ($tables as $table) {
            DB::delete('DELETE FROM '.$table);
        }
    }
        
    protected function loadLocale()
    {
        $this->locale = app()->getLocale();
        $this->info("Locale=".$this->locale);
        $this->biblioPath = base_path().'/biblio/'.$this->locale.'/';
        $this->info('Path='.$this->biblioPath);
    }

    protected function loadTests()
    {
        $this->info("Loading tests");

        $finder = new Finder();
        $finder->files()->name('*.yaml')->in($this->biblioPath.'/tests');

        DB::beginTransaction();
        $fields = ['id', 'name', 'desc', 'delay'];
        foreach ($finder as $file) {
            $content = Yaml::parseFile($file);
            $content = Arr::only($content, $fields);
            $content = array_values($content);
            DB::insert("INSERT INTO tests (id, name, desc, delay) VALUES (?, ?, ?, ?)", $content);
        }
        DB::commit();
    }

    protected function loadSymptoms()
    {
        $this->info("Loading symptoms");

        $finder = new Finder();
        $finder->files()->name('*.yaml')->in($this->biblioPath.'/symptoms');

        DB::beginTransaction();
        $fields = ['id', 'name', 'desc'];
        foreach ($finder as $file) {
            $content = Yaml::parseFile($file);
            $values = Arr::only($content, $fields);
            $values = array_values($values);
            DB::insert("INSERT INTO symptoms (id, name, desc, delay) VALUES (?, ?, ?, -1)", $values);
            
            if(isset($content['aka'])) {
                $content['aka'][] = $content['name'];
                foreach ($content['aka'] as $alias) {
                    DB::insert("INSERT INTO symptomsaka VALUES (?, ?)", [$content['id'], $alias]);
                }
            }

            if (isset($content['tests'])) {
                foreach ($content['tests'] as $test) {
                    DB::insert("INSERT INTO symptom_test VALUES (?, ?)", [$content['id'], $test]);
                }
            }
        }
        DB::commit();
    }

    protected function loadConditions()
    {
        $this->info("Loading conditions");

        $finder = new Finder();
        $finder->files()->name('*.yaml')->in($this->biblioPath.'/conditions');

        DB::beginTransaction();
        $fields = ['id', 'name', 'desc', 'urgency'];
        foreach ($finder as $file) {
            $content = Yaml::parseFile($file);
            $values = Arr::only($content, $fields);
            $values = array_values($values);
            DB::insert("INSERT INTO conditions (id, name, desc, urgency) VALUES (?, ?, ?, ?)", $values);

            if (isset($content['symptoms'])) {
                foreach ($content['symptoms'] as $symptom) {
                    DB::insert("INSERT INTO condition_symptom VALUES (?, ?)", [$content['id'], $symptom]);
                }
            }
        }
        DB::commit();
    }

    protected function fillData()
    {
        $this->info('Filling data');

        $this->fillMissingTestDelay();
        $this->fillMissingConditionUrgency();
        $this->fillSymptomDelay();
    }

    protected function fillMissingTestDelay()
    {
        $average = DB::select("SELECT avg(delay) AS avgdelay FROM tests WHERE delay >= 0");
        $average = intval($average[0]->avgdelay);
        DB::update("UPDATE tests SET delay = ? WHERE delay < 0", [$average]);
    }

    protected function fillMissingConditionUrgency()
    {
        $urgency = DB::select("SELECT avg(urgency) AS avgurgency FROM conditions WHERE urgency >= 0");
        $urgency = intval($urgency[0]->avgurgency);
        DB::update("UPDATE conditions SET urgency = ? WHERE urgency < 0", [$urgency]);
    }

    protected function fillSymptomDelay()
    {
        $sql = <<<EOL
            SELECT
                symptom_test.symptom_id AS symptom_id,
                min(tests.delay) AS delay
            FROM
                symptom_test
                JOIN tests ON symptom_test.test_id = tests.id
            GROUP BY
                symptom_test.symptom_id
        EOL;
        $delays = DB::select($sql);
        DB::beginTransaction();
        foreach ($delays as $delay) {
            DB::update("UPDATE symptoms SET delay = ? WHERE id = ?", [$delay->delay, $delay->symptom_id]);
        }
        DB::commit();       
    }

    protected function loadSuggestionsTable()
    {
        $sql = <<<EOL
            INSERT INTO
                suggestions
            SELECT
                conditions.id AS condition_id,
                conditions.name AS condition_name,
                conditions.urgency AS condition_urgency,
                symptoms.id AS symptom_id,
                symptoms.name AS symptom_name,
                symptoms.delay AS symptom_delay,
                tests.id AS test_id,
                tests.name AS test_name,
                tests.delay AS test_delay
            FROM
                conditions
                JOIN condition_symptom ON conditions.id = condition_symptom.condition_id
                JOIN symptoms ON symptoms.id = condition_symptom.symptom_id
                JOIN symptom_test ON symptoms.id = symptom_test.symptom_id
                JOIN tests ON tests.id = symptom_test.test_id
            ORDER BY
                conditions.urgency ASC,
                symptoms.delay ASC,
                tests.delay ASC
        EOL;

        DB::insert($sql);
    }
}
