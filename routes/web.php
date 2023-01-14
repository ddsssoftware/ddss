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
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\CaseController;
use App\Http\Controllers\SymptomController;
use App\Http\Controllers\ConditionController;
use App\Http\Controllers\TestController;
use App\Http\Controllers\FactsheetController;

Route::get('/', [CaseController::class, 'index'])->name('case.index');
Route::post('/description-update', [CaseController::class, 'updateDescription'])->name('case.description.update');
Route::get('/summary', [CaseController::class, 'summary'])->name('case.summary');

Route::get('/factsheet/condition/{id}', [FactsheetController::class, 'condition'])->name('factsheet.condition');
Route::get('/factsheet/symptom/{id}', [FactsheetController::class, 'symptom'])->name('factsheet.symptom');
Route::get('/factsheet/test/{id}', [FactsheetController::class, 'test'])->name('factsheet.test');

Route::get('/symptom-search', [SymptomController::class, 'search'])->name('case.symptom.search');
Route::post('/symptom-present', [SymptomController::class, 'present'])->name('case.symptom.present');
Route::post('/symptom-notpresent', [SymptomController::class, 'notPresent'])->name('case.symptom.notpresent');
Route::post('/symptom-remove', [SymptomController::class, 'remove'])->name('case.symptom.remove');

Route::get('/condition-search', [ConditionController::class, 'search'])->name('case.condition.search');
Route::post('/condition-present', [ConditionController::class, 'present'])->name('case.condition.present');
Route::post('/condition-notpresent', [ConditionController::class, 'notPresent'])->name('case.condition.notpresent');
Route::post('/condition-remove', [ConditionController::class, 'remove'])->name('case.condition.remove');

Route::post('/test-remove', [TestController::class, 'remove'])->name('case.test.remove');
Route::post('/test-add', [TestController::class, 'add'])->name('case.test.add');

