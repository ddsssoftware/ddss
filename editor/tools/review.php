<?php
include_once __DIR__ . '/../inc/header.php';
include_once __DIR__ . '/../inc/data.php';
?>

<h1 class="title">Review</h1>

<?php

function msg($msg, $clazz = '')
{
    echo '<p class="' . $clazz . '">' . date("H:m:s") . ' ' . $msg . '</p>' . PHP_EOL;
}

$diagnosesById = [];
$symptomsById = [];
$symptomsInUse = [];

msg('Checking duplicate diagnoses');

foreach ($diagnoses as $d) {
    $id = $d['id'];
    if (isset($diagnosesById[$id])) {
        msg('Duplicate id: ' . $id);
    } else {
        $diagnosesById[$id] = $d;
    }
}

msg('Checking duplicate symptoms');

foreach ($symptoms as $s) {
    $id = $s['id'];
    if (isset($symptomsById[$id])) {
        msg('Duplicate id: ' . $id);
    } else {
        $symptomsById[$id] = $s;
    }
}

msg('Checking symptoms keys');
foreach ($diagnoses as $d) {
    $symptomsInUse = array_merge($symptomsInUse, $d['symptoms']);
}
$symptomsInUse = array_unique($symptomsInUse);
$diff = array_diff($symptomsInUse, array_keys($symptomsById));
if (count($diff)) {
    msg("Symptoms used in diagnoses but not in symptoms file: " . implode(', ', $diff));
}
$diff = array_diff(array_keys($symptomsById), $symptomsInUse);
if (count($diff)) {
    msg("Symptoms not used in any diagnosis: " . implode(', ', $diff));
}

msg('Sorting diagnoses');
foreach ($diagnoses as &$d) {
    $s = $d['symptoms'];
    $s = array_unique($s);
    sort($s);
    $d['symptoms'] = $s;
}
usort($diagnoses, function ($a, $b) {
    return strcmp($a['id'], $b['id']);
});
saveDiagnoses();

msg('Sorting symptoms');
usort($symptoms, function ($a, $b) {
    return strcmp($a['id'], $b['id']);
});


?>


<?php include_once __DIR__ . '/../inc/footer.php'; ?>