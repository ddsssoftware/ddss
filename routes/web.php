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
use App\Http\Controllers\FactsheetController;

Route::get('/', [CaseController::class, 'index'])->name('case.index');
Route::post('/', [CaseController::class, 'updateDescription'])->name('case.updatedescription');

Route::get('/factsheet/condition/{id}', [FactsheetController::class, 'condition'])->name('factsheet.condition');
Route::get('/factsheet/symptom/{id}', [FactsheetController::class, 'symptom'])->name('factsheet.symptom');
Route::get('/factsheet/test/{id}', [FactsheetController::class, 'test'])->name('factsheet.test');

Route::post('/symptom-search', [SymptomController::class, 'search'])->name('case.symptom.search');

Route::post('/condition-search', [ConditionController::class, 'search'])->name('case.condition.search');
Route::post('/condition-present', [ConditionController::class, 'present'])->name('case.condition.present');