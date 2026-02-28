const Repository = {
    load: function () {
        if (!storageAvailable()) {
            alert("Enable session and local storage in your browser and try again. See logs for details");
            return
        }
        for (let dataType of ['diagnoses.json', 'symptoms.json']) {
            const url = '/data/' + dataType;
            fetch(url, 'HEAD')
                .then(response => {
                    const etagKey = response.url + "__ETAG__";
                    if (this.isExpired(etagKey, response)) {
                        fetch(url, 'GET')
                            .then(response => {
                                if (response.ok) {
                                    response.text()
                                        .then(body => {
                                            globalThis.localStorage.setItem(dataType, body);
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

    storageAvailable: function () {
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
    }
};
