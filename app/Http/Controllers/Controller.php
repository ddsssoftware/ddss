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

use Illuminate\Foundation\Auth\Access\AuthorizesRequests;
use Illuminate\Foundation\Bus\DispatchesJobs;
use Illuminate\Foundation\Validation\ValidatesRequests;
use Illuminate\Routing\Controller as BaseController;

class Controller extends BaseController
{
    use AuthorizesRequests, DispatchesJobs, ValidatesRequests;

    function collapseData(&$data, $conditionFlag = true, $symptomFlag = true, $testFlag = true)
    {
        if ($testFlag) {
            $keys = array_keys($data);
            $previousKey = $keys[0];
            foreach ($keys as $key) {
                if ($previousKey != $key &&
                    $data[$previousKey]->symptom_id == $data[$key]->symptom_id) {
                    if (!isset($data[$previousKey]->tests)) {
                        $data[$previousKey]->tests = [];
                    }
                    $data[$previousKey]->tests[] = $data[$key];
                    unset($data[$key]);
                } else {
                    if (!isset($data[$key]->tests)) {
                        $data[$key]->tests = [];
                        $data[$key]->tests[] = $data[$key];
                    }
                    $previousKey = $key;
                }
            }
        }
    }

    public function getCase($case)
    {
        $case = trim($case, '"');
        if ($case == 'new') {
            $case = [];
            $case['conditions'] = [];
        } else {
            $case = unserialize($case);
        }
        return $case;
    }
}
