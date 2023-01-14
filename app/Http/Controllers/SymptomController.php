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
use App\Models\Diagnosis;
use Illuminate\Routing\Controller;
use Illuminate\Foundation\Validation\ValidatesRequests;

class SymptomController extends Controller
{
    use ValidatesRequests;

    public function search(Request $request)
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

    public function remove(Request $request)
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

}
