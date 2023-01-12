<?php

namespace App\Models;

use Illuminate\Support\Facades\DB;

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

    public static function addTestsToSymptoms(&$symptoms)
    {
        $sql = <<<EOL
            SELECT
                tests.id,
                tests.name,
                symptom_test.symptom_id
            FROM
                tests
            JOIN symptom_test ON symptom_test.test_id = tests.id
            WHERE
                symptom_test.symptom_id IN (?)
            ORDER BY
                tests.delay ASC
        EOL;
        $sql = str_replace('?', implode(',', array_column($symptoms, 'id')), $sql);
        $tests = DB::select($sql);
        self::mergeData($symptoms, 'id', $tests, 'symptom_id', 'tests');
    }

    public static function mergeData(&$set1, $key1, &$set2, $key2, $attribute)
    {
        foreach ($set1 as $item1) {
            if (!isset($item1->$attribute)) {
                $item1->$attribute = [];
            }
            foreach ($set2 as $item2) {
                if ($item1->$key1 == $item2->$key2) {
                    $item1->$attribute[] = $item2;
                }
            }
        }
    }

    public static function suggestConditions(&$case)
    {
        $conditions = DB::table('conditions')
            ->select('conditions.id', 'conditions.name')
            ->orderBy('conditions.urgency', 'ASC')
            ->get();

        return $conditions;
    }

}