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

use App\Models\Test;
use Illuminate\Foundation\Validation\ValidatesRequests;
use Illuminate\Http\Request;
use Illuminate\Routing\Controller;
use Illuminate\Support\Facades\DB;

class TestController extends Controller
{
    use ValidatesRequests;

    private $rules = [
        'name' => 'required|max:'.Test::NAME_SIZE_MAX,
        'desc' => 'required',
        'delay' => 'required',
    ];

    public function index()
    {
        $tests = Test::select('id', 'name')->orderBy('name')->get();

        return view('tests.index', compact('tests'));
    }

    public function create()
    {
        return view('tests.create');
    }

    public function store(Request $request)
    {
        Test::create($request->validate($this->rules));

        return redirect(route('tests.index'));
    }

    public function show($id)
    {
        $test = Test::findOrFail($id);

        return view('tests.show', compact('test'));
    }

    public function edit($id)
    {
        $test = Test::findOrFail($id);

        return view('tests.edit', compact('test'));
    }

    public function update(Request $request, $id)
    {
        $test = Test::findOrFail($id);

        $test->update($request->validate($this->rules));

        return redirect(route('tests.update', $test));
    }

    public function destroy($id)
    {
        $test = Test::findOrFail($id);

        DB::transaction(function () use ($test) {
            $test->symptoms()->detach();
            $test->delete();
        });

        return redirect(route('tests.index'));
    }
}
