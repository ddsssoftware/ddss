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

class CaseController extends Controller
{
    public function index()
    {
        return view('index');
    }

    public function updateDescription(Request $request)
    {
        extract($request->validate([
            'case' => ['bail', 'required'],
            'description' => ['bail', 'string'],
        ]));
        $case = $this->getCase($case);
        $case['description'] = $description;

        return view('index', compact('case'));
    }
}
