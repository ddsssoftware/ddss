<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class BiblioMakeCommand extends Command
{
    protected $signature = 'biblio:make {type} {name?}';

    protected $description = 'Create a template for types: condition, symptom, test';

    public function __construct()
    {
        parent::__construct();
    }

    public function handle()
    {
        $type = $this->checkParam();
        $name = $this->argument('name');

        return $type == null ? 1 : $this->template($type, $name);
    }

    private function checkParam()
    {
        $supported = ['condition', 'symptom', 'test'];
        $type = $this->argument('type');

        if (in_array($type, $supported)) {
            return $type;
        } else {
            $this->info('Type not supported='.$type);
            $this->info('Supported types='.implode(', ', $supported));

            return null;
        }
    }

    private function template($type, $name)
    {
        $id = $this->getMaxId($type);
        $template = base_path('resources/templates/'.$type.'.yaml');
        $filename = $this->getFilename($id, $type, $name);
        $template = file_get_contents($template);
        $template = str_replace('?', $id, $template);
        $name = '"'.($name ?? '').'"';
        $template = str_replace('$', $name, $template);
        file_put_contents($filename, $template);
        $this->info('Created file='.$filename);

        return 0;
    }

    private function getMaxId($type)
    {
        $max = DB::select("SELECT MAX(id) AS id FROM {$type}s")[0]->id;

        return intval($max) + 1;
    }

    private function getFilename($id, $type, $name)
    {
        $locale = app()->getLocale();
        $filename = str_pad($id, 9, '0', STR_PAD_LEFT);
        $filename = chunk_split($filename, 3, '_');
        $filename .= $name == null ? $type : Str::slug($name);
        $filename = base_path('biblio/'.$locale.'/'.$type.'s/'.$filename.'.yaml');

        return $filename;
    }
}
