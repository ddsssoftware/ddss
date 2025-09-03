<?php
include_once __DIR__ . '/../inc/header.php';
include_once __DIR__ . '/../inc/data.php';

$symptomsJs = PHP_EOL . 'new gridjs.Grid({columns: ["ID", "Name", {name:"Actions",formatter: (_, row) => gridjs.html("<a href=\"/symptoms/edit.php?id="+row.cells[0].data+"\">Edit</a>")}],search:true,pagination:true,' . PHP_EOL;
$symptomsJs .= 'data: [' . PHP_EOL;
foreach ($symptoms as $sym) {
    $symptomsJs .= '["' . $sym['id'] . '","' . $sym['name'] . '"],' . PHP_EOL;
}
$symptomsJs .= ']}).render(document.getElementById("symptoms_table_wrapper"));' . PHP_EOL;
?>
<script src="https://cdn.jsdelivr.net/npm/gridjs/dist/gridjs.umd.js"></script>
<h1 class="title">Symptoms <a href="/symptoms/create.php" class="button is-link">New</a></h1>
<div id="symptoms_table_wrapper"></div>
<script><?= $symptomsJs ?></script>

<?php include_once __DIR__ . '/../inc/footer.php'; ?>