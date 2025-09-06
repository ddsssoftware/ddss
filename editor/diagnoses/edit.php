<?php
include_once __DIR__ . '/../inc/header.php';
include_once __DIR__ . '/../inc/data.php';

$diagnosis = getDiagnosisById($_GET['id'])['value'];
?>
<h1 class="title">Diagnosis <?= $diagnosis['name'] ?></h1>
<form action="/diagnoses/patch.php" method="POST">
    <?php include_once __DIR__ . '/form.php'; ?>
    <div class="field">
        <button class="button is-link">Save</button>
        <a href="" class="button is-danger has-text-primary-100">Reset</a>
    </div>
</form>

<?php include_once __DIR__ . '/../inc/footer.php'; ?>