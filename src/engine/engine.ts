
class Engine {

    private readonly repository: Repository;
    private diagnoses: Diagnosis[];
    private symptoms: Symptom[];
    private diagnosesByIndex: Map<string, Diagnosis>;
    private symptomsByIndex: Map<string, Symptom>;
    private diagnosesBySymptom: Map<string, Diagnosis[]>

    public constructor(repository: Repository) {
        this.repository = repository;
        this.loadDataStructures();
    }

    private loadDataStructures(): void {
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

    public suggest(caze: Case): CaseSuggestion {
        return null;
    }

}

class CaseSuggestion {
    public diagnoes: Diagnosis[];
    public symptoms: Symptom[];
}