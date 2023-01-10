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

class TestController extends Controller
{
    public function add(Request $request)
    {
        extract($request->validate([
            'test' => ['bail', 'required', 'exists:tests,id'],
            'case' => ['bail', 'required'],
            'notes' => ['bail', 'nullable', 'string'],
        ]));

        $sql = <<<EOL
            SELECT
                tests.id,
                tests.name,
                tests.delay
            FROM
                tests
            WHERE
                tests.id = ?
        EOL;
        $data = DB::select($sql, [$test])[0];
        $data->notes = htmlentities($notes);
        $case = $this->loadCase($case);
        $case['tests'][$test] = $data;
        $savedCase = $this->saveCase($case);

        return view('index', compact('case', 'savedCase'));
    }

    public function remove(Request $request)
    {
        extract($request->validate([
            'case' => ['bail', 'required'],
            'test' => ['bail', 'required', 'integer'],
        ]));

        $case = $this->loadCase($case);
        unset($case['tests'][$test]);
        $savedCase = $this->saveCase($case);

        return view('index', compact('case', 'savedCase'));
    }
}
