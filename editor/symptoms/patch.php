<?php

include_once __DIR__ . '/../inc/data.php';

$symptom = getSymptomById($_POST['id']);
$symptom['value']['name'] = $_POST['name'];

saveSymptom($symptom);

header('Location: ' . getBaseUrl() . '/symptoms/edit.php?id=' . $symptom['value']['id']);