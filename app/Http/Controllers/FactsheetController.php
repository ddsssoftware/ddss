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

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Routing\Controller;

class FactsheetController extends Controller
{
    public function condition($id)
    {
        $condition = DB::select("SELECT * FROM conditions WHERE id = ?", [$id]);

        if (count($condition) == 0) abort(404);
        $condition = $condition[0];

        $sql = <<<EOL
            SELECT
                symptoms.id,
                symptoms.name
            FROM
                symptoms
                JOIN condition_symptom ON condition_symptom.symptom_id = symptoms.id
            WHERE
                condition_symptom.condition_id = ?
            ORDER BY
                symptoms.delay
        EOL;
        $symptoms = DB::select($sql, [$id]);

        $sql = <<<EOL
            SELECT DISTINCT
                tests.id,
                tests.name,
                tests.delay
            FROM
                tests
                JOIN symptom_test ON tests.id = symptom_test.test_id
                JOIN condition_symptom ON condition_symptom.symptom_id = symptom_test.symptom_id
                JOIN conditions ON conditions.id = condition_symptom.condition_id
            WHERE
                conditions.id = ?
            ORDER BY
                tests.delay ASC
        EOL;
        $tests = DB::select($sql, [$id]);

        return view('factsheets.condition', compact('condition', 'symptoms', 'tests'));
    }

    public function symptom($id)
    {
        $symptom = DB::select("SELECT * FROM symptoms WHERE id = ?", [$id]);

        if (count($symptom) == 0) abort(404);
        $symptom = $symptom[0];

        $sql = <<<EOL
            SELECT
                tests.id,
                tests.name
            FROM
                tests
                JOIN symptom_test ON symptom_test.test_id = tests.id
            WHERE
                symptom_test.symptom_id = ?
            ORDER BY
                tests.delay ASC
        EOL;
        $tests = DB::select($sql, [$id]); 

        $sql = <<<EOL
            SELECT
                conditions.id,
                conditions.name
            FROM
                conditions
                JOIN condition_symptom ON condition_symptom.condition_id = conditions.id
            WHERE
                condition_symptom.symptom_id = ?
            ORDER BY
                conditions.urgency ASC
        EOL;
        $conditions = DB::select($sql, [$id]);

        return view('factsheets.symptom', compact('symptom', 'tests', 'conditions'));
    }

    public function test($id)
    {
        $test = DB::select("SELECT * FROM tests WHERE id = ?", [$id]);

        if (count($test) == 0) abort(404);
        $test = $test[0];

        $sql = <<<EOL
            SELECT
                symptoms.id,
                symptoms.name
            FROM
                symptoms
                JOIN symptom_test ON symptom_test.symptom_id = symptoms.id
            WHERE
                symptom_test.test_id = ?
        EOL;
        $symptoms = DB::select($sql, [$id]); 

        $sql = <<<EOL
            SELECT DISTINCT
                conditions.id,
                conditions.name,
                conditions.urgency
            FROM
                conditions
                JOIN condition_symptom ON condition_symptom.condition_id = conditions.id
                JOIN symptom_test ON condition_symptom.symptom_id = symptom_test.symptom_id
            WHERE
                symptom_test.test_id = ?
            ORDER BY
                conditions.urgency
        EOL;
        $conditions = DB::select($sql, [$id]); 

        return view('factsheets.test', compact('test', 'symptoms', 'conditions'));
    }
}
