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

use Illuminate\Routing\Controller;
use Illuminate\Foundation\Validation\ValidatesRequests;
use Illuminate\Http\Request;
use App\Models\Diagnosis;

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
        } else {
            $case = Diagnosis::new();
            $suggestedConditions = null;
            $savedCase = Diagnosis::save($case);
        }
        
        return view('index', compact('case', 'savedCase', 'suggestedConditions'));
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
}
