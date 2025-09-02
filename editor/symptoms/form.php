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