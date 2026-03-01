// #region Search
const Search = function () {
    return {
        /**
         * Searches for symptoms with names that match partially the given term.
         * Case insensitive.
         * 
         * @param {string} term - Term to match
         * 
         * @returns {array} A list of symptoms that matches term
         */
        symptoms(term) {
            let symptoms = [];

            if (typeof term === "string") {
                term = term.toLowerCase();
                symptoms = Repository.symptoms().filter(symptom => 
                        symptom.name &&
                        typeof symptom.name === "string" &&
                        symptom.name.toLowerCase().includes(term)
                    );
            }

            return symptoms;
        },

        diagnoses(term) {
            //TODO
        }
    }
}();
// #endregion