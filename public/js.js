//#region Util

String.prototype.hashCode = function() {
    var hash = 0,
    i, chr;
    if (this.length === 0) return hash;
    for (i = 0; i < this.length; i++) {
        chr = this.charCodeAt(i);
        hash = ((hash << 5) - hash) + chr;
        hash |= 0;
    }

    return hash;
}

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
    inputEl.setAttribute('value', JSON.stringify(document.ddsscase));
    formEl.appendChild(inputEl);
}

//#endregion


//#region Case

setupDescriptionUnsavedAlert();
document.addEventListener("beforeunload", checkDescriptionUnsaved);

function setupDescriptionUnsavedAlert() {
    el = document.getElementById("case_description_form_text");
    el.dataset.hash = el.innerText.hashCode();
}

function checkDescriptionUnsaved() {
    //TODO: test with HTTPS
    el = document.getElementById("case_description_form_text");
    if (el.dataset.hash != el.innerText.hashCode()) {
        return "Case description changes will not be saved";
    }
}

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

document.querySelectorAll('.condition_item_details_presence_form_button').forEach(el => {
    el.addEventListener('click', function(event) {
        formId = event.target.id.replace('_button', '');
        console.log(formId);
        formEl = document.getElementById(formId);
        addCaseToForm(formEl);
        formEl.submit();
    });
});

//#endregion