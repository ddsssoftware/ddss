class Repository {

    public static readonly DIAGNOSES_JSON: string = 'diagnoses.json';
    public static readonly SYMPTOMS_JSON: string = 'symptoms.json';
    private static readonly HEAD_METHOD: RequestInit = { method: 'HEAD' };
    private static readonly GET_METHOD: RequestInit = { method: 'GET' };

    public constructor() {
        this.init();
    }

    public init(): void {
        if (!this.storageAvailable()) {
            alert("Enable session and local storage in your browser and try again. See logs for details");

            return;
        }

        this.loadData();

        if (!this.checkIntegrity()) {
            alert("Data integrity check failed. See logs for details.");
        }
    }

    private loadData() {
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
                                } else {
                                    this.httpLogError('Response not ok ' + response.status + ' ' + response.statusText);
                                }
                            }, this.httpLogError)
                            .catch(this.httpLogError);
                    }
                }, this.httpLogError)
                .catch(this.httpLogError);
        }
    }

    private isExpired(etagKey: string, response: Response): boolean {
        return !response.ok
            || response.headers.get('ETag') == null
            || globalThis.localStorage.getItem(etagKey) == null
            || response.headers.get('ETag') != globalThis.localStorage.getItem(etagKey);
    }

    private httpLogError(reason: any) {
        alert('Failed to make http request. See logs for details.');
        console.error(reason);
    }

    private checkIntegrity(): boolean {
        return true;
    }

    private storageAvailable(): boolean {
        let available: boolean = false;

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

    public getDiagnoses(): Diagnosis[] {
        return JSON.parse(globalThis.localStorage.getItem(Repository.DIAGNOSES_JSON)) as Diagnosis[];
    }

    public getSymptoms(): Symptom[] {
        return JSON.parse(globalThis.localStorage.getItem(Repository.SYMPTOMS_JSON)) as Symptom[];
    }

}
