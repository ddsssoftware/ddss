// #region SymptomsSearchComponent
const SymptomsSearchComponent = function () {
    const SYMPTOMS_RESULTS_ID = symptoms__datalist_search;
    return {
        search(event) {
            const term = event.target.value;
            let symptoms = [];
            if (term.length > 1) {
                symptoms = Search.symptoms(term);
            }
            this.fill(symptoms);
        },

        fill(symptoms) {
            const $resultsDiv = document.getElementById(SYMPTOMS_RESULTS_ID);
        }
    }
}();
// #endregion

// #region SymptomItem
class SymptomItem extends HTMLElement {

    constructor() {
        super();
    }

    connectedCallback() {
        const root = this.attachShadow({ mode: 'closed' });
        root.innerHTML = `
            <button hx-get="/my-component-clicked" hx-target="next div">Click me!</button>
            <div></div>
            `;
        htmx.process(root);
    }
}

customElements.define('symptom-item', SymptomItem);
// #endregion

// #region DiagnosesSearchComponent
const DiagnosesSearchComponent = function () {

}();
// #endregion