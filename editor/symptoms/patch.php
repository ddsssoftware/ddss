<?php

include_once __DIR__ . '/../inc/data.php';

$symptomEntry = getSymptomById($_POST['id']);
$symptomEntry['value']['name'] = $_POST['name'];

saveSymptom($symptomEntry);

if (isset($_POST['diagnosisid'])) {
    $diagnosisEntry = getDiagnosisById($_POST['diagnosisid']);
    $diagnosisEntry['value']['symptoms'][] = $symptomEntry['value']['id'];
    saveDiagnosis($diagnosisEntry);
}

header('Location: ' . getBaseUrl() . '/symptoms/edit.php?id=' . $symptomEntry['value']['id']);