<?php

require_once __DIR__ . '/lib.php';

$diagnoses = json_decode(file_get_contents($DIAGNOSES_FILE_PATH), true);
$symptoms = json_decode(file_get_contents($SYMPTOMS_FILE_PATH), true);