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

namespace App\Http\Controllers;

use App\Models\Diagnosis;
use Illuminate\Foundation\Validation\ValidatesRequests;
use Illuminate\Http\Request;
use Illuminate\Routing\Controller;
use Illuminate\Support\Facades\DB;

class CaseController extends Controller
{
    use ValidatesRequests;

    public function index(Request $request)
    {
        extract($request->validate([
            'c' => ['bail', 'nullable', 'string'],
        ]));
        if (isset($c)) {
            $case = Diagnosis::load($c);
            $savedCase = $c;
            $suggestedConditions = Diagnosis::suggestConditions($case);
            $suggestedSymptoms = Diagnosis::suggestSymptoms($case, $suggestedConditions);
        } else {
            $case = Diagnosis::new();
            $suggestedConditions = null;
            $suggestedSymptoms = null;
            $savedCase = Diagnosis::save($case);
        }

        return view('index', compact('case', 'savedCase', 'suggestedConditions', 'suggestedSymptoms'));
    }

    public function updateDescription(Request $request)
    {
        extract($request->validate([
            'c' => ['bail', 'required'],
            'description' => ['bail', 'nullable', 'string'],
        ]));
        $case = Diagnosis::load($c);
        $case[Diagnosis::DESCRIPTION] = $description;
        $c = Diagnosis::save($case);

        return redirect()->route('case.index', compact('c'));
    }

    public function summary(Request $request)
    {
        extract($request->validate([
            'c' => ['bail', 'required'],
        ]));
        $case = Diagnosis::load($c);
        $savedCase = $c;

        return view('case.synopsis', compact('case', 'savedCase'));
    }

    public function conditionSearch(Request $request)
    {
        extract($request->validate([
            'term' => ['bail', 'required', 'string', 'min:1'],
            'c' => ['bail', 'required'],
        ]));
        $conditionSearchResult = DB::table('conditions')
            ->select('conditions.id', 'conditions.name')
            ->join('conditionsaka', 'conditions.id', '=', 'conditionsaka.condition_id')
            ->where('conditionsaka.searchname', 'LIKE', '%'.strtolower($term).'%')
            ->orderBy('conditions.urgency')
            ->distinct()
            ->get();
        $case = Diagnosis::load($c);
        $savedCase = $c;

        return view('index', compact('conditionSearchResult', 'case', 'savedCase'));
    }

    public function conditionPresent(Request $request)
    {
        return $this->conditionPresence($request, true);
    }

    public function conditionNotPresent(Request $request)
    {
        return $this->conditionPresence($request, false);
    }

    public function conditionPresence(Request $request, $present)
    {
        extract($request->validate([
            'condition' => ['bail', 'required', 'exists:conditions,id'],
            'c' => ['bail', 'required'],
            'notes' => ['bail', 'nullable', 'string'],
        ]));
        $data = (array) DB::table('conditions')
            ->select('conditions.name AS n')
            ->where('conditions.id', '=', $condition)
            ->first();
        $data[Diagnosis::PRESENCE] = $present;
        $data[Diagnosis::NOTES] = htmlentities($notes);
        $case = Diagnosis::load($c);
        $case[Diagnosis::CONDITIONS][$condition] = $data;
        $c = Diagnosis::save($case);

        return redirect()->route('case.index', compact('c'));
    }

    public function conditionRemove(Request $request)
    {
        extract($request->validate([
            'c' => ['bail', 'required'],
            'condition' => ['bail', 'required', 'integer'],
        ]));

        $case = Diagnosis::load($c);
        unset($case[Diagnosis::CONDITIONS][$condition]);
        $c = Diagnosis::save($case);

        return redirect()->route('case.index', compact('c'));
    }

    public function symptomSearch(Request $request)
    {
        extract($request->validate([
            'term' => ['bail', 'required', 'string', 'min:1'],
            'c' => ['bail', 'required'],
        ]));
        $symptomSearchResult = DB::table('symptoms')
            ->select('symptoms.id', 'symptoms.name')
            ->join('symptomsaka', 'symptoms.id', '=', 'symptomsaka.symptom_id')
            ->where('symptomsaka.searchname', 'LIKE', '%'.strtolower($term).'%')
            ->orderBy('symptoms.urgency', 'ASC')
            ->orderBy('symptoms.delay', 'ASC')
            ->distinct()
            ->get();
        Diagnosis::addTestsToSymptoms($symptomSearchResult);
        $case = Diagnosis::load($c);
        $savedCase = Diagnosis::save($case);

        return view('index', compact('symptomSearchResult', 'case', 'savedCase'));
    }

    public function symptomPresent(Request $request)
    {
        return $this->symptomPresence($request, true);
    }

    public function notPresent(Request $request)
    {
        return $this->symptomPresence($request, false);
    }

    public function symptomPresence(Request $request, $present)
    {
        extract($request->validate([
            'symptom' => ['bail', 'required', 'exists:symptoms,id'],
            'c' => ['bail', 'required'],
            'notes' => ['bail', 'nullable', 'string'],
        ]));
        $data = (array) DB::table('symptoms')
            ->select('symptoms.name AS n')
            ->where('symptoms.id', '=', $symptom)
            ->first();
        $data[Diagnosis::PRESENCE] = $present;
        $data[Diagnosis::NOTES] = htmlentities($notes);
        $case = Diagnosis::load($c);
        $case[Diagnosis::SYMPTOMS][$symptom] = $data;
        $c = Diagnosis::save($case);

        return redirect()->route('case.index', compact('c'));
    }

    public function symptomRemove(Request $request)
    {
        extract($request->validate([
            'c' => ['bail', 'required'],
            'symptom' => ['bail', 'required', 'integer'],
        ]));

        $case = Diagnosis::load($c);
        unset($case[Diagnosis::SYMPTOMS][$symptom]);
        $c = Diagnosis::save($case);

        return redirect()->route('case.index', compact('c'));
    }

    public function testAdd(Request $request)
    {
        extract($request->validate([
            'test' => ['bail', 'required', 'exists:tests,id'],
            'c' => ['bail', 'required'],
            'notes' => ['bail', 'nullable', 'string'],
        ]));

        $sql = <<<'EOL'
            SELECT
                tests.name AS n
            FROM
                tests
            WHERE
                tests.id = ?
        EOL;
        $data = (array) DB::select($sql, [$test])[0];
        $data[Diagnosis::NOTES] = htmlentities($notes);
        $case = Diagnosis::load($c);
        $case[Diagnosis::TESTS][$test] = $data;
        $c = Diagnosis::save($case);

        return redirect()->route('case.index', compact('c'));
    }

    public function testRemove(Request $request)
    {
        extract($request->validate([
            'c' => ['bail', 'required'],
            'test' => ['bail', 'required', 'integer'],
        ]));

        $case = Diagnosis::load($c);
        unset($case[Diagnosis::TESTS][$test]);
        $c = Diagnosis::save($case);

        return redirect()->route('case.index', compact('c'));
    }
}
