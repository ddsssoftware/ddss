<?php

$DIAGNOSES_FILE_PATH = __DIR__ . '/../../public/data/diagnoses.json';
$SYMPTOMS_FILE_PATH = __DIR__ . '/../../public/data/symptoms.json';

function slug($str)
{
    $str = strtolower($str);
    $str = preg_replace('/[^a-z0-9]+/i', '-', $str);
    $str = trim($str, '-');

    return $str;
}


