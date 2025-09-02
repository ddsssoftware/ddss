<?php
include_once __DIR__ . '/../inc/header.php';
include_once __DIR__ . '/../inc/data.php';

$diagnosesJs = PHP_EOL . 'new gridjs.Grid({columns: ["ID", "ICD", "Name", {name:"Actions",formatter: (_, row) => gridjs.html("<a href=\"/diagnoses/edit.php?id="+row.cells[0].data+"\">Edit</a>")}],search:true,pagination:true,' . PHP_EOL;
$diagnosesJs .= 'data: [' . PHP_EOL;
foreach ($diagnoses as $diag) {
    $diagnosesJs .= '["' . $diag['id'] . '","' . $diag['icd'] . '","' . $diag['name'] . '"],' . PHP_EOL;
}
$diagnosesJs .= ']}).render(document.getElementById("diagnoses_table_wrapper"));' . PHP_EOL;
?>
<h1 class="title">Diagnoses <a href="/diagnoses/create.php" class="button is-link">New</a></h1>
<div id="diagnoses_table_wrapper"></div>
<script><?= $diagnosesJs ?></script>

<?php include_once __DIR__ . '/../inc/footer.php'; ?>