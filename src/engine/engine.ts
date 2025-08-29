
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

    public suggest(caze: Case): CaseSuggestion {
        return null;
    }

}

class CaseSuggestion {
    public diagnoes: Diagnosis[];
    public symptoms: Symptom[];
}