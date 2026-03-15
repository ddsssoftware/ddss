// #region SymptomsSearchComponent
const SymptomsSearchComponent = function () {
    const SYMPTOMS_RESULTS_ID = 'symptoms__results';
    return {
        search(event) {
            const term = event.target.value;
            let symptoms = [];
            if (term.length > 1) {
                symptoms = Search.symptoms(term);
            }
            this.fill(symptoms);
        },

        /**
         * 
         * @param {array<Symptom>} symptoms 
         */
        fill(symptoms) {
            const $resultsDiv = document.getElementById(SYMPTOMS_RESULTS_ID);
            for (const s of symptoms) {
                $resultsDiv.appendChild(new SymptomItem(s));
            }
        }
    }
}();
// #endregion

// #region SymptomItem
class SymptomItem extends HTMLElement {

    /** @type {Symptom} */
    symptom;

    /**
     * 
     * @param {Symptom} symptom
     */
    constructor(symptom) {
        super();
        this.symptom = symptom;
        const $spanName = document.createElement('span');
        $spanName.textContent = symptom.name;
        const $btnAdd = document.createElement('button');
        $btnAdd.textContent = 'Adicionar';
        $btnAdd.classList.add('button');
        this.appendChild($spanName);
        this.appendChild($btnAdd);
    }

}

customElements.define('symptom-item', SymptomItem);
// #endregion

// #region DiagnosesSearchComponent
const DiagnosesSearchComponent = function () {

}();
// #endregion

// #region CaseComponent
const CaseComponent = function() {
    return {
        /**
         * 
         * @param {Symptom} symptom 
         */
        addSymptom(symptom) {

        }
    }
};