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

function getDiagnosisById(string $id): array|null
{
    global $diagnoses;
    $d = null;
    foreach ($diagnoses as $key => $value) {
        if ($value['id'] == $id) {
            $d = compact('key', 'value');
            break;
        }
    }

    return $d;
}

function saveDiagnoses($diagnosisEntry)
{
    global $diagnoses, $DIAGNOSES_FILE_PATH;
    $diagnoses[$diagnosisEntry['key']] = $diagnosisEntry['value'];

    file_put_contents($DIAGNOSES_FILE_PATH, json_encode($diagnoses, JSON_PRETTY_PRINT));
}

function getUrl()
{
    $uri = $_SERVER['REQUEST_URI'];

    return getBaseUrl() . $uri;
}

function getBaseUrl()
{
    $protocol = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? "https" : "http";

    $host = $_SERVER['HTTP_HOST'];

    return $protocol . "://" . $host;
}


