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

class ConditionController extends Controller
{
    public function search(Request $request)
    {
        $conditionSearchResult = [];
        if (isset($request->term)) {
            $term = $request->term;
            if (strlen($term) != 0) {
                $term = '%'.strtolower($term).'%';
                $sql = <<<EOL
                    SELECT DISTINCT
                        conditions.id,
                        conditions.name,
                        conditions.urgency
                    FROM
                        conditionsaka
                        JOIN conditions ON conditions.id = conditionsaka.condition_id
                    WHERE
                        conditionsaka.name LIKE ?
                    ORDER BY
                        conditions.urgency
                EOL;
                $conditionSearchResult = DB::select($sql, [$term]);    
            }
        }

        return view('index', compact('conditionSearchResult'));
    }

    public function present(Request $request)
    {
        extract($request->validate([
            'condition' => ['bail', 'required', 'exists:conditions,id'],
            'case' => ['bail', 'required'],
        ]));
        $sql = <<<EOL
            SELECT
                conditions.id,
                conditions.name,
                conditions.urgency
            FROM
                conditions
            WHERE
                conditions.id = ?
        EOL;
        $data = DB::select($sql, [$condition])[0];
        $data->present = true;
        $case = $this->getCase($case);
        $case['conditions'][$condition] = $data;

        return view('index', compact('case'));
    }
}
