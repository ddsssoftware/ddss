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

use App\Models\Symptom;
use Illuminate\Foundation\Validation\ValidatesRequests;
use Illuminate\Http\Request;
use Illuminate\Routing\Controller;
use Illuminate\Support\Facades\DB;

class SymptomController extends Controller
{
    use ValidatesRequests;

    private $rules = [
        'name' => 'required|max:'.Symptom::NAME_SIZE_MAX,
        'desc' => 'required',
        'delay' => 'required',
        'urgency' => 'required',
    ];

    public function index()
    {
        $symptoms = Symptom::select('id', 'name')->orderBy('name')->get();

        return view('symptoms.index', compact('symptoms'));
    }

    public function create()
    {
        return view('symptoms.create');
    }

    public function store(Request $request)
    {
        Symptom::create($request->validate($this->rules));

        return redirect(route('symptoms.index'));
    }

    public function show($id)
    {
        $symptom = Symptom::findOrFail($id);

        return view('symptoms.show', compact('symptom'));
    }

    public function edit($id)
    {
        $symptom = Symptom::findOrFail($id);

        return view('symptoms.edit', compact('symptom'));
    }

    public function update(Request $request, $id)
    {
        $symptom = Symptom::findOrFail($id);

        $symptom->update($request->validate($this->rules));

        return redirect(route('symptoms.update', $symptom));
    }

    public function destroy($id)
    {
        $symptom = Symptom::findOrFail($id);

        DB::transaction(function () use ($symptom) {
            $symptom->conditions()->detach();
            $symptom->tests()->detach();
            $symptom->aka()->delete();
            $symptom->delete();
        });

        return redirect(route('symptoms.index'));
    }
}
