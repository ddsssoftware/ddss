<pre><?php

include_once __DIR__ . '/../inc/data.php';

$diagnosis = [];
$diagnosis['id'] = slug($_POST['name']);
$diagnosis['icd'] = $_POST['icd'];
$diagnosis['name'] = $_POST['name'];

addDiagnosis($diagnosis);

header('Location: ' . getBaseUrl() . '/diagnoses/edit.php?id=' . $diagnosis['id']);