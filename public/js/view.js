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
            console.log(symptoms);
            for (const s of symptoms) {
                console.log(s);
            }
        }
    }
}();
// #endregion

// #region SymptomItem
class SymptomItem extends HTMLElement {

    static TEMPLATE_ID = 'template__symptom_id';
    symptom;

    constructor() {
        super();
    }

    connectedCallback() {
        const root = this.attachShadow({ mode: 'closed' });
        const template = document.getElementById(TEMPLATE_ID).content.cloneNode(true);
        root.append(template);
        htmx.process(root);
    }
}

customElements.define('symptom-item', SymptomItem);
// #endregion

// #region DiagnosesSearchComponent
const DiagnosesSearchComponent = function () {

}();
// #endregion