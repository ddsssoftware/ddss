<input class="input" type="hidden" name="id" value="<?= isset($symptom) ? $symptom['id'] : '' ?>">
<div class="field">
    <label class="label">ID</label>
    <div class="control">
        <input class="input" type="text" name="id" value="<?= isset($symptom) ? $symptom['id'] : '' ?>" disabled>
    </div>
</div>
<div class="field">
    <label class="label">Name</label>
    <div class="control">
        <input class="input" type="text" name="name" value="<?= isset($symptom) ? $symptom['name'] : '' ?>" required>
    </div>
</div>
<div class="field pb-6">
    <span class="label">Associate with diagnosis</span>
    <div class="control radios is-block">
        <?php foreach (array_slice($diagnoses, -5, 5) as $d)
            echo '<label class="radio is-block pl-3"><input type="radio" class="mr-3" name="diagnosisid" value="' . $d['id'] . '" />' . $d['name'] . '</label>' . PHP_EOL;
        ?>
    </div>
</div>