<?php

namespace App\Models;

use Illuminate\Support\Facades\DB;

abstract class Diagnosis
{
    public const DESCRIPTION = 'd';

    public const SYMPTOMS = 's';

    public const TESTS = 't';

    public const CONDITIONS = 'c';

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
        $tests = DB::table('tests')
            ->select('tests.id', 'tests.name', 'symptom_test.symptom_id')
            ->join('symptom_test', 'symptom_test.test_id', '=', 'tests.id')
            ->whereIn('symptom_test.symptom_id', $symptoms->pluck('id'))
            ->orderBy('tests.delay', 'ASC')
            ->get();
        self::mergeData($symptoms, 'id', $tests, 'symptom_id', 'tests');
    }

    public static function mergeData(&$set1, $key1, &$set2, $key2, $attribute)
    {
        foreach ($set1 as $item1) {
            if (! isset($item1->$attribute)) {
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
        $caseConditions = collect($case[self::CONDITIONS]);
        $caseSymptoms = collect($case[self::SYMPTOMS]);
        $conditions = DB::table('conditions')
            ->select('conditions.id', 'conditions.name')
            ->join('condition_symptom', 'condition_symptom.condition_id', '=', 'conditions.id')
            ->whereNotIn('conditions.id', $caseConditions->where(self::PRESENCE, '=', false)->keys())
            ->whereIn('condition_symptom.symptom_id', $caseSymptoms->where(self::PRESENCE, '=', true)->keys())
            ->orderBy('conditions.urgency', 'ASC')
            ->distinct()
            ->get();

        return $conditions;
    }

    public static function suggestSymptoms(&$case, &$suggestedConditions)
    {
        $caseSymptoms = array_keys($case[self::SYMPTOMS]);

        $symptoms = DB::table('symptoms')
            ->select('symptoms.id', 'symptoms.name')
            ->join('condition_symptom', 'condition_symptom.symptom_id', '=', 'symptoms.id')
            ->whereNotIn('symptoms.id', $caseSymptoms)
            ->whereIn('condition_symptom.condition_id', $suggestedConditions->pluck('id'))
            ->orderBy('symptoms.urgency', 'ASC')
            ->orderBy('symptoms.delay', 'ASC')
            ->distinct()
            ->get();

        Diagnosis::addTestsToSymptoms($symptoms);

        return $symptoms;
    }
}
