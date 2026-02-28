class Symptom {
}
class SymptomEntry {
}
class Diagnosis {
}
class DiagnosisEntry {
}
class Case {
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
        for (let dataType of [Repository.DIAGNOSES_JSON, Repository.SYMPTOMS_JSON]) {
            const url = '/data/' + dataType;
            fetch(url, Repository.HEAD_METHOD)
                .then(response => {
                const etagKey = response.url + "__ETAG__";
                if (this.isExpired(etagKey, response)) {
                    fetch(url, Repository.GET_METHOD)
                        .then(response => {
                        if (response.ok) {
                            response.text()
                                .then(body => {
                                globalThis.localStorage.setItem(dataType, body);
                                globalThis.localStorage.setItem(etagKey, response.headers.get('ETag'));
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
        }
    }
    isExpired(etagKey, response) {
        return !response.ok
            || response.headers.get('ETag') == null
            || globalThis.localStorage.getItem(etagKey) == null
            || response.headers.get('ETag') != globalThis.localStorage.getItem(etagKey);
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
            const x = "__STORAGE__TEST__";
            for (let storage of [globalThis.localStorage, globalThis.sessionStorage]) {
                storage.setItem(x, x);
                storage.removeItem(x);
            }
            available = true;
        }
        catch (err) {
            console.error(err);
        }
        return available;
    }
    getDiagnoses() {
        return JSON.parse(globalThis.localStorage.getItem(Repository.DIAGNOSES_JSON));
    }
    getSymptoms() {
        return JSON.parse(globalThis.localStorage.getItem(Repository.SYMPTOMS_JSON));
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
        for (let d of this.diagnoses) {
            this.diagnosesByIndex.set(d.id, d);
            for (let s of d.symptoms) {
                if (!this.diagnosesBySymptom.has(s.id)) {
                    this.diagnosesBySymptom.set(s.id, []);
                }
                this.diagnosesBySymptom.get(s.id).push(d);
            }
        }
        for (let s of this.symptoms) {
            this.symptomsByIndex.set(s.id, s);
        }
    }
    suggest(caze) {
        return null;
    }
}
class CaseSuggestion {
}
class Controller {
    constructor(engine) {
        this.engine = engine;
    }
    ;
}
class Component {
    constructor(id, caze, controller) {
        this.id = id;
        this.caze = caze;
        this.controller = controller;
    }
    getElement() {
        return document.getElementById(this.id);
    }
}
class NewButtonComponent extends Component {
    constructor(caze, controller) {
        super("sys__new", caze, controller);
    }
    reset() {
        throw new Error("Method not implemented.");
    }
    innit() {
        this.getElement().addEventListener('click', this.onClick.bind(this));
    }
    onClick() {
        throw new Error("Method not implemented.");
    }
}
class NotesComponent extends Component {
    constructor(caze, controller) {
        super("case__notes", caze, controller);
    }
    innit() {
        this.getElement().addEventListener('input', this.onInput.bind(this));
    }
    reset() {
        this.getElement().value = this.caze.notes;
    }
    onInput(event) {
        const target = event.target;
        this.caze.notes = target.value;
    }
}
class SymptomsSearchComponent extends Component {
    constructor(caze, controller) {
        super("symptoms__input_search", caze, controller);
    }
    reset() {
        throw new Error("Method not implemented.");
    }
    innit() {
        this.getElement().addEventListener('input', this.onInput.bind(this));
    }
    onInput() {
    }
}
let engine = new Engine(new Repository());
let controller = new Controller(engine);
console.log("DDSS ready");
//# sourceMappingURL=app.js.map