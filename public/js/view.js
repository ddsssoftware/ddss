// #region SymptomsSearchComponent
const SymptomsSearchComponent = function() {
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
            
        }
    }
}();
// #endregion

// #region DiagnosesSearchComponent
const DiagnosesSearchComponent = function() {

}();
// #endregion