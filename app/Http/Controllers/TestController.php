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
use Illuminate\Support\Facades\DB;
use App\Models\Diagnosis;

class TestController extends Controller
{
    use ValidatesRequests;

    public function add(Request $request)
    {
        extract($request->validate([
            'test' => ['bail', 'required', 'exists:tests,id'],
            'c' => ['bail', 'required'],
            'notes' => ['bail', 'nullable', 'string'],
        ]));

        $sql = <<<EOL
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

    public function remove(Request $request)
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
