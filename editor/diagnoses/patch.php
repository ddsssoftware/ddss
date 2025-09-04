<?php

include_once __DIR__ . '/../inc/data.php';

$diagnosis = getDiagnosisById($_POST['id']);
$diagnosis['value']['icd'] = $_POST['icd'];
$diagnosis['value']['name'] = $_POST['name'];
$s = array_unique($_POST['symptom']);
sort($s);
$diagnosis['value']['symptoms'] = $s;

saveDiagnosis($diagnosis);

header('Location: ' . getBaseUrl() . '/diagnoses/edit.php?id=' . $diagnosis['value']['id']);