<?php
include_once __DIR__ . '/../inc/header.php';
include_once __DIR__ . '/../inc/data.php';

?>
<h1 class="title">New symptom</h1>
<form action="/symptoms/post.php" method="POST">
    <?php include_once __DIR__ . '/form.php'; ?>
    <div class="field">
        <button class="button is-link">Save</button>
    </div>
</form>

<?php include_once __DIR__ . '/../inc/footer.php'; ?>