<?php
include_once __DIR__ . '/../inc/header.php';
include_once __DIR__ . '/../inc/data.php';

$diagnosis = getDiagnosisById($_GET['id']);
?>
<h1 class="title">Diagnosis <?= $diagnosis['name'] ?></h1>
<form action="/diagnoses/patch" method="POST">
    <?php include_once __DIR__ . '/form.php'; ?>
    <div class="field">
        <button class="button is-link">Save</button>
    </div>
</form>

<?php include_once __DIR__ . '/../inc/footer.php'; ?>