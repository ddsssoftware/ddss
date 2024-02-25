<?php
/**
 *   Differential Diagnosis Support System
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
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\DB;
use Symfony\Component\Finder\Finder;

class BiblioImportCommand extends Command
{
    public const DEFAULT_LOCALE = 'en';

    protected $signature = 'ddss:import {locale?}';

    protected $description = 'Import files into database';

    public $tables = ['conditions', 'symptoms', 'tests', 'condition_symptom', 'symptom_test', 'conditionsaka', 'symptomsaka'];

    public $filenames = [];

    private $locale;

    private $biblioPath;

    private $dbPath;

    public function __construct()
    {
        parent::__construct();
        $this->finder = new Finder();
    }

    public function handle()
    {
        $this->info('Started DDSS import');

        $this->loadLocale();
        if ($this->dbExist()) {
            $this->warn('Please remove database file and try again');

            return Command::FAILURE;
        }
        if (! $this->filesExist()) {
            $this->warn('Please create file and try again');

            return Command::FAILURE;
        }

        if ($this->createDb() === false) {
            $this->warn('Could not create database');

            return Command::FAILURE;
        }

        $this->importTables();

        $this->info('Ended DDSS import');

        return Command::SUCCESS;
    }

    protected function loadLocale()
    {
        $this->locale = $this->argument('locale') ?? self::DEFAULT_LOCALE;
        $this->info('Locale='.$this->locale);
        $this->biblioPath = base_path().'/biblio/'.$this->locale.'/';
        $this->info('Path='.$this->biblioPath);
        $this->dbPath = config('database.connections.sqlite.database');
        $this->info('DB='.$this->dbPath);
    }

    protected function dbExist()
    {
        $exists = file_exists($this->dbPath);

        if ($exists) {
            $this->warn('Database already exists. Please remove and try again');
        }

        return $exists;
    }

    protected function filesExist()
    {
        foreach ($this->tables as $table) {
            $file = $this->biblioPath.$table.'.csv';
            if (! file_exists($file)) {
                $this->warn("File not found $file");

                return false;
            }
            $this->filenames[$table] = $file;
        }

        return true;
    }

    protected function createDb()
    {
        $this->info('Creating tables');

        $ok = touch($this->dbPath);
        if ($ok !== false) {
            $ok = Artisan::call('migrate', ['--force' => true]) == 0;
        }

        return $ok;
    }

    protected function importTables()
    {
        $this->info('Importing tables');

        DB::beginTransaction();

        foreach ($this->filenames as $table => $filename) {
            $this->info("t $table f $filename");
            $fh = fopen($filename, 'r');
            if ($fh == false) {
                $this->warn("Could not open file $filename");

                return false;
            }
            while (($data = fgetcsv($fh, 0, BiblioExportCommand::FIELD_SEPARATOR)) !== false) {
                if ($data == null) {
                    continue;
                }
                $sql = $sql ?? "INSERT INTO $table VALUES (".implode(', ', array_fill(0, count($data), '?')).')';
                DB::insert($sql, $data);
            }
            $sql = null;
            fclose($fh);
        }

        DB::commit();

        return true;
    }
}
