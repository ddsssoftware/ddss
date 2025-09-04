<script src="/diagnoses/form.js"></script>
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
<div class="field">
    <label class="label">Symptom</label>
    <div class="control">
        <input class="input" type="text" list="symptoms" autocomplete="off" id="symptomslist">
        <datalist id="symptoms">
            <?php
            foreach ($symptoms as $s) {
                $d = $s['name'] . ' / ' . $s['id'];
                echo '<option value="' . $d . '" data-symptomid="' . $s['id'] . '">' . $d . '</option>' . PHP_EOL;
            }
            ?>
        </datalist>
    </div>
    <div class="control p-3 ml-3">
        <table class="table is-striped is-hoverable is-bordered" id="symptomtable">
            <?php
            foreach ($diagnosis['symptoms'] as $s) {
                $d = ' data-symptomid="' . $s . '" ';
                echo '<tr><td><input type="hidden" name="symptom[]" value="' . $s . '"' . $d . '><span class="has-text-weight-normal"' . $d . '>' . $s . '</span></td><td><span ' . $d . ' class="is-clickable">&#x2715;</span></td></tr>' . PHP_EOL;
            }
            ?>
        </table>
    </div>
</div>