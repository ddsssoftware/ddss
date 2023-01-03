<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\CaseController;

Route::get('/', [CaseController::class, 'index'])->name('case.index');
