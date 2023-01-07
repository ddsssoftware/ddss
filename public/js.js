//#region Util

function toggle(el) {
    if (el.style.display == 'none') {
        el.style.display = '';
    } else {
        el.style.display = 'none';
    }
}

function addCaseToForm(formEl) {
    inputEl = document.createElement('input');
    inputEl.setAttribute('type', 'hidden');
    inputEl.setAttribute('name', 'case');
    inputEl.setAttribute('value', document.ddsscase);
    formEl.appendChild(inputEl);
}

document.querySelectorAll('[data-form-needs-case="true"]').forEach(el => {
    el.addEventListener('click', function(event) {
        formId = event.target.id.replace('_submit', '');
        formEl = document.getElementById(formId);
        addCaseToForm(formEl);
        formEl.submit();
    });
});

//#endregion


//#region Case

//#endregion

//#region Symptoms

document.querySelectorAll('.symptom_item_name').forEach(el => {
    el.addEventListener('click', function(event) {
        id = event.target.id.replace('name', 'details');
        toggle(document.getElementById(id));
    });
});

//#endregion

//#region Conditions

document.querySelectorAll('.condition_item_name').forEach(el => {
    el.addEventListener('click', function(event) {
        id = event.target.id.replace('name', 'details');
        toggle(document.getElementById(id));
    });
});

//#endregion