class Symptom {
}
class SymptomEntry {
}
class Diagnosis {
}
class DiagnosisEntry {
}
class Case {
    getPresentSymptoms() {
        return this.getSymptomsByPresence(Presence.Present);
    }
    getSymptomsByPresence(presence) {
        return this.symptoms.filter(symptomEntry => {
            return symptomEntry.presence == presence;
        }).map(symptomEntry => {
            return symptomEntry.symptom;
        });
    }
}
var Presence;
(function (Presence) {
    Presence["Present"] = "Present";
    Presence["NotPresent"] = "Not Present";
    Presence["Unknown"] = "Unknown";
})(Presence || (Presence = {}));
class Repository {
    constructor() {
        this.init();
    }
    init() {
        if (!this.storageAvailable()) {
            alert("Enable session and local storage in your browser and try again. See logs for details");
            return;
        }
        this.loadData();
        if (!this.checkIntegrity()) {
            alert("Data integrity check failed. See logs for details.");
        }
    }
    loadData() {
        const dataTypes = [Repository.DIAGNOSES_JSON, Repository.SYMPTOMS_JSON];
        dataTypes.forEach(dataType => {
            const url = '/data/' + dataType;
            fetch(url, Repository.HEAD_METHOD)
                .then(response => {
                if (this.isExpired(response)) {
                    fetch(url, Repository.GET_METHOD)
                        .then(response => {
                        if (response.ok) {
                            response.text()
                                .then(body => {
                                window.localStorage.setItem(dataType, body);
                            }, this.httpLogError)
                                .catch(this.httpLogError);
                        }
                        else {
                            this.httpLogError('Response not ok ' + response.status + ' ' + response.statusText);
                        }
                    }, this.httpLogError)
                        .catch(this.httpLogError);
                }
            }, this.httpLogError)
                .catch(this.httpLogError);
        });
    }
    isExpired(response) {
        const key = response.url + "__ETAG__";
        return !response.ok
            || response.headers.get('ETag') == null
            || window.localStorage.getItem(key) == null
            || response.headers.get('ETag') != window.localStorage.getItem(key);
    }
    httpLogError(reason) {
        alert('Failed to make http request. See logs for details.');
        console.error(reason);
    }
    checkIntegrity() {
        return true;
    }
    storageAvailable() {
        let available = false;
        try {
            const storages = [window.localStorage, window.sessionStorage];
            const x = "__STORAGE__TEST__";
            storages.forEach(storage => {
                storage.setItem(x, x);
                storage.removeItem(x);
            });
            available = true;
        }
        catch (err) {
            console.error(err);
        }
        return available;
    }
    getDiagnoses() {
        return JSON.parse(window.localStorage.getItem(Repository.DIAGNOSES_JSON));
    }
    getSymptoms() {
        return JSON.parse(window.localStorage.getItem(Repository.SYMPTOMS_JSON));
    }
}
Repository.DIAGNOSES_JSON = 'diagnoses.json';
Repository.SYMPTOMS_JSON = 'symptoms.json';
Repository.HEAD_METHOD = { method: 'HEAD' };
Repository.GET_METHOD = { method: 'GET' };
class Engine {
    constructor(repository) {
        this.repository = repository;
        this.loadDataStructures();
    }
    loadDataStructures() {
        this.diagnoses = this.repository.getDiagnoses();
        this.symptoms = this.repository.getSymptoms();
        this.diagnoses.forEach(diagnosis => {
            this.diagnosesByIndex.set(diagnosis.id, diagnosis);
            diagnosis.symptoms.forEach(symptom => {
                if (!this.diagnosesBySymptom.has(symptom.id)) {
                    this.diagnosesBySymptom.set(symptom.id, []);
                }
                this.diagnosesBySymptom.get(symptom.id).push(diagnosis);
            });
        });
        this.symptoms.forEach(symptom => {
            this.symptomsByIndex.set(symptom.id, symptom);
        });
    }
    suggest(caze) {
        const present = caze.getPresentSymptoms();
        const diagnoses = new Set();
        present.forEach(symptom => {
            this.diagnosesBySymptom.get(symptom.id).forEach(diagnoses.add, diagnoses);
        });
        return new CaseSuggestion(Array.from(diagnoses.values()), present);
    }
}
class CaseSuggestion {
    constructor(diagnoses, symptoms) {
        this.diagnoses = diagnoses;
        this.symptoms = symptoms;
    }
}
class Controller {
    constructor(engine) {
        this.engine = engine;
    }
}
let engine = new Engine(new Repository());
let controller = new Controller(engine);
console.log("DDSS ready");
//# sourceMappingURL=app.js.map