<?php

include_once __DIR__ . '/../inc/data.php';

$symptom = [];
$symptom['id'] = slug($_POST['name']);
$symptom['name'] = $_POST['name'];

addSymptom($symptom);

header('Location: ' . getBaseUrl() . '/symptoms/edit.php?id=' . $symptom['id']);