<?php

namespace App\Models;

abstract class Diagnosis {

    public const DESCRIPTION = 'd';
    public const SYMPTOMS = 's';
    public const TESTS = 't';
    public const CONDITIONS = 'c';

    public const ID = 'i';
    public const NAME = 'n';
    public const PRESENCE = 'p';
    public const NOTES = 'c';

    public static function new()
    {
        $diagnosis = [];
        $diagnosis[self::DESCRIPTION] = '';
        $diagnosis[self::SYMPTOMS] = [];
        $diagnosis[self::TESTS] = [];
        $diagnosis[self::CONDITIONS] = [];
        
        return $diagnosis;
    }

    public static function load($saved)
    {
        $saved = base64_decode($saved);
        $saved = gzuncompress($saved);
        $saved = json_decode($saved, true);

        return $saved;
    }

    public static function save($diagnosis)
    {
        $diagnosis = json_encode($diagnosis);        
        $diagnosis = gzcompress($diagnosis, 9);
        $diagnosis = base64_encode($diagnosis);

        return $diagnosis;
    }

    public static function collapseData(&$data, $conditionFlag = true, $symptomFlag = true, $testFlag = true)
    {
        if ($testFlag) {
            $keys = array_keys($data);
            $previousKey = $keys[0];
            foreach ($keys as $key) {
                if ($previousKey != $key &&
                    $data[$previousKey]->symptom_id == $data[$key]->symptom_id) {
                    if (!isset($data[$previousKey]->tests)) {
                        $data[$previousKey]->tests = [];
                    }
                    $data[$previousKey]->tests[] = $data[$key];
                    unset($data[$key]);
                } else {
                    if (!isset($data[$key]->tests)) {
                        $data[$key]->tests = [];
                        $data[$key]->tests[] = $data[$key];
                    }
                    $previousKey = $key;
                }
            }
        }
    }




}