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
        const dataTypes: string[] = [Repository.DIAGNOSES_JSON, Repository.SYMPTOMS_JSON];
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
                                } else {
                                    this.httpLogError('Response not ok ' + response.status + ' ' + response.statusText);
                                }
                            }, this.httpLogError)
                            .catch(this.httpLogError);
                    }
                }, this.httpLogError)
                .catch(this.httpLogError);
        });
    }

    private isExpired(response: Response): boolean {
        const key = response.url + "__ETAG__";
        return !response.ok
            || response.headers.get('ETag') == null
            || window.localStorage.getItem(key) == null
            || response.headers.get('ETag') != window.localStorage.getItem(key);
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
            const storages: Storage[] = [window.localStorage, window.sessionStorage];
            const x = "__STORAGE__TEST__";
            storages.forEach(storage => {
                storage.setItem(x, x);
                storage.removeItem(x);
            });

            available = true;
        } catch (err) {
            console.error(err);
        }

        return available;
    }

    public getDiagnoses(): Diagnosis[] {
        return JSON.parse(window.localStorage.getItem(Repository.DIAGNOSES_JSON)) as Diagnosis[];
    }

    public getSymptoms(): Symptom[] {
        return JSON.parse(window.localStorage.getItem(Repository.SYMPTOMS_JSON)) as Symptom[];
    }

}
