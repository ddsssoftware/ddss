// #region Repository
const Repository = function () {
    /** @type {array} */
    let symptoms = [];
    /** @type {array} */
    let diagnoses = [];

    return {
        load: function () {
            if (!this.isStorageAvailable()) {
                alert("Enable session and local storage in your browser and try again. See logs for details");
                return
            }
            const jsonFiles = ['diagnoses.json', 'symptoms.json'];
            for (let jsonFile of jsonFiles) {
                const url = '/data/' + jsonFile;
                console.log(url);
                fetch(url, { method: 'HEAD' })
                    .then(response => {
                        const etagKey = jsonFile + "__ETAG__";
                        if (this.isExpired(etagKey, response)) {
                            fetch(url, { method: 'GET' })
                                .then(response => {
                                    if (response.ok) {
                                        response.text()
                                            .then(body => {
                                                globalThis.localStorage.setItem(jsonFile, body);
                                                globalThis.localStorage.setItem(etagKey, response.headers.get('ETag'));
                                            }, this.httpLogError)
                                            .catch(this.httpLogError);
                                    } else {
                                        this.httpLogError('Response not ok ' + response.status + ' ' + response.statusText);
                                    }
                                }, this.httpLogError)
                                .catch(this.httpLogError);
                        }
                    }, this.httpLogError)
                    .catch(this.httpLogError);
            }


        },

        isExpired: function (etagKey, response) {
            return !response.ok
                || response.headers.get('ETag') == null
                || globalThis.localStorage.getItem(etagKey) == null
                || response.headers.get('ETag') != globalThis.localStorage.getItem(etagKey);
        },

        httpLogError: function (reason) {
            alert('Failed to make http request. See logs for details.');
            console.error(reason);
        },

        isStorageAvailable: function () {
            let available = false;

            try {
                const x = "__STORAGE__TEST__";
                for (let storage of [globalThis.localStorage, globalThis.sessionStorage]) {
                    storage.setItem(x, x);
                    storage.removeItem(x);
                }

                available = true;
            } catch (err) {
                console.error(err);
            }

            return available;
        },

        diagnoses: function () {
            return this.diagnoses;
        },

        /**
         * Returns all symptoms in the repository
         * 
         * @returns {array} List of symptoms
         */
        symptoms: function () {
            return this.symptoms;
        }
    }
}();
// #endregion

// #region Case
const Case = function () {

}();
// #endregion