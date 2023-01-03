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

//#endregion



//#region Case

document.getElementById("case_digital-summary_copy-to-clipboard").addEventListener("click", copyToClipboard);
document.getElementById("case_digital-summary_continue-previous").addEventListener("click", showContinuePrevious);
document.getElementById("case_digital-summary_form_cancel").addEventListener("click", hideContinuePrevious);
setupDescriptionUnsavedAlert();
document.addEventListener("beforeunload", checkDescriptionUnsaved);

function setupDescriptionUnsavedAlert() {
    el = document.getElementById("case_description-form_text");
    el.dataset.hash = el.innerText.hashCode();
}

function checkDescriptionUnsaved() {
    //TODO: test with HTTPS
    el = document.getElementById("case_description-form_text");
    if (el.dataset.hash != el.innerText.hashCode()) {
        return "Case description changes will not be saved";
    }
}

function copyToClipboard() {
    navigator.clipboard.writeText(document.getElementById("case_digital-summary_summary").innerText);
}

function showContinuePrevious() {
    toggle(document.getElementById("case_digital-summary_form"));
}

function hideContinuePrevious() {
    toggle(document.getElementById("case_digital-summary_form"));
}

//#endregion

