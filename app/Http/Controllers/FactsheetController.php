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
        EOL;
        $symptoms = DB::select($sql, [$id]); 

        return view('factsheets.condition', compact('condition', 'symptoms'));
    }

    public function symptom($id)
    {

    }

    public function test($id)
    {

    }
}
