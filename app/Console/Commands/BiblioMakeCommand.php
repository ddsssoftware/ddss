<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;

class BiblioMakeCommand extends Command
{
    protected $signature = 'biblio:make {type}';


    protected $description = 'Create a template for types: condition, symptom, test';

    public function __construct()
    {
        parent::__construct();
    }

    public function handle()
    {
        $type = $this->checkParam();
        return $type == null ? 1 : $this->template($type);
    }

    private function checkParam()
    {
        $supported = ['condition', 'symptom', 'test'];
        $type = $this->argument('type');

        if (in_array($type, $supported)) {
            return $type;
        } else {
            $this->info("Type not supported=".$type);
            $this->info("Supported types=".implode(', ', $supported));
            return null;
        }
    }

    private function template($type)
    {
        $table = $type.'s';
        $id = $this->getMaxId($table);
        $template = base_path('resources/templates/'.$type.'.yaml');
        $filename = $this->getFilename($id, $type, $table);
        $template = file_get_contents($template);
        $template = str_replace('?', $id, $template);
        file_put_contents($filename, $template);
        $this->info('Created file='.$filename);

        return 0;
    }

    private function getMaxId($table)
    {
        $max = DB::select("SELECT MAX(id) AS id FROM $table")[0]->id;
        return intval($max) + 1;
    }

    private function getFilename($id, $type, $table) {
        $locale = app()->getLocale();
        $filename = str_pad($id, 9, '0', STR_PAD_LEFT);
        $filename = chunk_split($filename, 3, '_');
        $filename = base_path('biblio/'.$locale.'/'.$table.'/'.$filename.$type.'.yaml');
        
        return $filename;
    }
}
