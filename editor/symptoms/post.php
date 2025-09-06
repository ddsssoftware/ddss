<?php

include_once __DIR__ . '/../inc/data.php';

$symptom = [];
$symptom['id'] = slug($_POST['name']);
$symptom['name'] = $_POST['name'];

addSymptom($symptom);

if (isset($_POST['diagnosisid'])) {
    $diagnosisEntry = getDiagnosisById($_POST['diagnosisid']);
    $diagnosisEntry['value']['symptoms'][] = $symptom['id'];
    saveDiagnosis($diagnosisEntry);
}

header('Location: ' . getBaseUrl() . '/symptoms/edit.php?id=' . $symptom['id']);