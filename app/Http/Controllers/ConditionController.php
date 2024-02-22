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

class ConditionController extends Controller
{
    use ValidatesRequests;

    public function search(Request $request)
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
        $savedCase = Diagnosis::save($case);

        return view('index', compact('conditionSearchResult', 'case', 'savedCase'));
    }

    public function present(Request $request)
    {
        return $this->presence($request, true);
    }

    public function notPresent(Request $request)
    {
        return $this->presence($request, false);
    }

    public function presence(Request $request, $present)
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

    public function remove(Request $request)
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
}
