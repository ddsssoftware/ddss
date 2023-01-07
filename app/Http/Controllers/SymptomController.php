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

class SymptomController extends Controller
{
    public function search(Request $request)
    {
        extract($request->validate([
            'term' => ['bail', 'required', 'string', 'min:1'],
            'case' => ['bail', 'required'],
        ]));
        $sql = <<<EOL
            SELECT
                suggestions.symptom_id,
                suggestions.symptom_name,
                suggestions.test_id,
                suggestions.test_name
            FROM
                suggestions
            WHERE
                suggestions.symptom_id IN (
                        SELECT
                            symptomsaka.symptom_id
                        FROM
                            symptomsaka
                        WHERE
                            name LIKE ?
                    )
        EOL;
        $term = '%'.strtolower($term).'%';
        $symptomSearchResult = DB::select($sql, [$term]);
        $this->collapseData($symptomSearchResult, false, false, true);
        $case = $this->getCase($case);

        return view('index', compact('symptomSearchResult', 'case'));
    }
}
