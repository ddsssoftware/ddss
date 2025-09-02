<?php
include_once __DIR__ . '/../inc/header.php';
include_once __DIR__ . '/../inc/data.php';

$symptom = getSymptomById($_GET['id'])['value'];
?>
<h1 class="title">Symptom <?= $symptom['name'] ?></h1>
<form action="/symptoms/patch.php" method="POST">
    <?php include_once __DIR__ . '/form.php'; ?>
    <div class="field">
        <button class="button is-link">Save</button>
    </div>
</form>

<?php include_once __DIR__ . '/../inc/footer.php'; ?>