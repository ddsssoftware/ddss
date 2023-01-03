<?php
/**
 *   Differential Diagnose Support System
 *   Copyright (C) 2023  ddss@gmail.com

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
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateSuggestionsTable extends Migration
{
    public function up()
    {
        Schema::create('suggestions', function (Blueprint $table) {
            $table->unsignedBigInteger('condition_id');
            $table->string('condition_name');
            $table->integer('condition_urgency');
            $table->unsignedBigInteger('symptom_id');
            $table->string('symptom_name');
            $table->integer('symptom_delay');
            $table->unsignedBigInteger('test_id');
            $table->string('test_name');
            $table->integer('test_delay');

            $table->index('condition_id');
            $table->index('symptom_id');
            $table->index('test_id');
        });
    }

    public function down()
    {
        Schema::dropIfExists('suggestions');
    }
}
