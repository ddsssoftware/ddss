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

use App\Models\Condition;
use Illuminate\Foundation\Validation\ValidatesRequests;
use Illuminate\Http\Request;
use Illuminate\Routing\Controller;
use Illuminate\Support\Facades\DB;

class ConditionController extends Controller
{
    use ValidatesRequests;

    private $rules = [
        'name' => 'required|max:'.Condition::NAME_SIZE_MAX,
        'desc' => 'required',
        'urgency' => 'required',
    ];

    public function index()
    {
        $conditions = Condition::select('id', 'name')->orderBy('name')->get();

        return view('conditions.index', compact('conditions'));
    }

    public function create()
    {
        return view('conditions.create');
    }

    public function store(Request $request)
    {
        Condition::create($request->validate($this->rules));

        return redirect(route('conditions.index'));
    }

    public function show($id)
    {
        $condition = Condition::findOrFail($id);

        return view('conditions.show', compact('condition'));
    }

    public function edit($id)
    {
        $condition = Condition::findOrFail($id);

        return view('conditions.edit', compact('condition'));
    }

    public function update(Request $request, $id)
    {
        $condition = Condition::findOrFail($id);

        $condition->update($request->validate($this->rules));

        return redirect(route('conditions.update', $condition));
    }

    public function destroy($id)
    {
        $condition = Condition::findOrFail($id);

        DB::transaction(function () use ($condition) {
            $condition->symptoms()->detach();
            $condition->aka()->delete();
            $condition->delete();
        });

        return redirect(route('conditions.index'));
    }
}
