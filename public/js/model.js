// #region Repository
const Repository = function () {

    /** @type {array} */
    const jsonFiles = ['diagnoses.json', 'symptoms.json'];
    /** @type {array} */
    let symptoms = [];
    /** @type {array} */
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
         * @returns {array} List of diagnoses
         */
        diagnoses() {
            return diagnoses;
        },

        /**
         * Returns all symptoms in the repository
         * 
         * @returns {array} List of symptoms
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