<input class="input" type="hidden" name="id" value="<?= isset($diagnosis) ? $diagnosis['id'] : '' ?>">
<div class="field">
    <label class="label">ID</label>
    <div class="control">
        <input class="input" type="text" name="id" value="<?= isset($diagnosis) ? $diagnosis['id'] : '' ?>" disabled>
    </div>
</div>
<div class="field">
    <label class="label">ICD</label>
    <div class="control">
        <input class="input" type="text" name="icd" value="<?= isset($diagnosis) ? $diagnosis['icd'] : '' ?>" required>
    </div>
</div>
<div class="field">
    <label class="label">Name</label>
    <div class="control">
        <input class="input" type="text" name="name" value="<?= isset($diagnosis) ? $diagnosis['name'] : '' ?>" required>
    </div>
</div>