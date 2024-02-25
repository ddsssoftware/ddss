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
use Illuminate\Support\Facades\DB;
use Symfony\Component\Finder\Finder;

class BiblioExportCommand extends Command
{
    public const DEFAULT_LOCALE = 'en';

    public const FIELD_SEPARATOR = "\t";

    protected $signature = 'ddss:export {locale?}';

    protected $description = 'Export database to files';

    public $tables = ['conditions', 'symptoms', 'tests', 'condition_symptom', 'symptom_test', 'conditionsaka', 'symptomsaka'];

    public $filenames = [];

    private $locale;

    private $biblioPath;

    public function __construct()
    {
        parent::__construct();
        $this->finder = new Finder();
    }

    public function handle()
    {
        $this->info('Started DDSS export');

        $this->loadLocale();
        if ($this->doFilesExist()) {
            $this->warn('Please remove file and try again');

            return Command::FAILURE;
        }
        $this->exportTables();

        $this->info('Ended DDSS export');

        return Command::SUCCESS;
    }

    protected function loadLocale()
    {
        $this->locale = $this->argument('locale') ?? self::DEFAULT_LOCALE;
        $this->info('Locale='.$this->locale);
        $this->biblioPath = base_path().'/biblio/'.$this->locale.'/';
        $this->info('Path='.$this->biblioPath);
    }

    protected function doFilesExist()
    {
        foreach ($this->tables as $table) {
            $file = $this->biblioPath.$table.'.csv';
            if (file_exists($file)) {
                $this->warn("File already exists $file");

                return true;
            }
            $this->filenames[$table] = $file;
        }

        return false;
    }

    protected function exportTables()
    {
        foreach ($this->tables as $table) {
            $filename = $this->filenames[$table];
            $fh = fopen($filename, 'w');
            if ($fh === false) {
                $this->warn("Could not open $filename");

                continue;
            }
            $rows = DB::table($table)->get()->toArray();
            foreach ($rows as $row) {
                fputcsv($fh, (array) $row, self::FIELD_SEPARATOR);
            }
            fflush($fh);
            fclose($fh);
        }

    }
}
