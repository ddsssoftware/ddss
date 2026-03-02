// #region Symptom
class Symptom {
    /** @type {string} */
    id;
    /** @type {string} */
    name;

    /**
     * Creates a new symptom from a json string or object
     * 
     * @param {string|any} json - Source json
     * @returns {Symptom} New Symptom object based on source
     */
    static from(json) {
        if (typeof json === "string") {
            JSON.parse(parse);
        }
        return Object.assign(new Symptom, json);
    }
}
// #endregion

// #region Diagnosis
class Diagnosis {

}
// #endregion

// #region Repository
const Repository = function () {

    /** @type {array} */
    const jsonFiles = ['diagnoses.json', 'symptoms.json'];
    /** @type {array<Symptom>} */
    let symptoms = [];
    /** @type {array<Diagnosis>} */
    let diagnoses = [];

    return {
        load() {
            for (let jsonFile of jsonFiles) {
                const url = '/data/' + jsonFile;
                fetch(url)
                    .then(response => {
                        if (response.ok) {
                            response.json()
                                .then(body => {
                                    if (jsonFile === jsonFile[0]) {
                                        diagnoses = body;
                                    } else {
                                        symptoms = body;
                                    }
                                }, this.httpLogError)
                                .catch(this.httpLogError);
                        } else {
                            this.httpLogError('Response not ok ' + response.status + ' ' + response.statusText);
                        }
                    }, this.httpLogError)
                    .catch(this.httpLogError);
            }
        },

        httpLogError(reason) {
            alert('Failed to make http request. See logs for details.');
            console.error(reason);
        },

        /**
         * Returns all diagnoses in the repository
         * 
         * @returns {array<Diagnosis>} List of diagnoses
         */
        diagnoses() {
            return diagnoses;
        },

        /**
         * Returns all symptoms in the repository
         * 
         * @returns {array<Symptom>} List of symptoms
         */
        symptoms() {
            return symptoms;
        }
    }
}();
// #endregion

// #region Case
const Case = function () {

}();
// #endregion