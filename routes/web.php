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
use App\Http\Controllers\CaseController;
use App\Http\Controllers\ConditionController;
use App\Http\Controllers\SymptomController;
use App\Http\Controllers\TestController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return redirect()->route('case.index');
});

Route::get('/case', [CaseController::class, 'index'])->name('case.index');
Route::post('/case/description', [CaseController::class, 'updateDescription'])->name('case.description.update');
Route::get('/case/summary', [CaseController::class, 'summary'])->name('case.summary');
Route::get('/case/symptom/search', [CaseController::class, 'symptomSearch'])->name('case.symptom.search');
Route::post('/case/symptom/present', [CaseController::class, 'symptompresent'])->name('case.symptom.present');
Route::post('/case/symptom/notpresent', [caseController::class, 'symptomNotPresent'])->name('case.symptom.notpresent');
Route::post('/case/symptom/remove', [CaseController::class, 'symptomRemove'])->name('case.symptom.remove');
Route::get('/case/condition/search', [CaseController::class, 'conditionSearch'])->name('case.condition.search');
Route::post('/case/condition/present', [CaseController::class, 'conditionPresent'])->name('case.condition.present');
Route::post('/case/condition/notpresent', [CaseController::class, 'conditionNotPresent'])->name('case.condition.notpresent');
Route::post('/case/condition/remove', [CaseController::class, 'conditionRemove'])->name('case.condition.remove');
Route::post('/case/test/remove', [CaseController::class, 'testRemove'])->name('case.test.remove');
Route::post('/case/test/-add', [CaseController::class, 'testAdd'])->name('case.test.add');

Route::resource('conditions', ConditionController::class);
Route::resource('symptoms', SymptomController::class);
Route::resource('tests', TestController::class);
