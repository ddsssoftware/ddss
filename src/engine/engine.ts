
class Engine {

    private readonly repository: Repository;
    private diagnoses: Diagnosis[];
    private symptoms: Symptom[];
    private diagnosesByIndex: Map<string, Diagnosis>;
    private symptomsByIndex: Map<string, Symptom>;

    public constructor(repository: Repository) {
        this.repository = repository;
        this.loadDataStructures();
    }

    private loadDataStructures(): void {
        this.diagnoses = this.repository.getDiagnoses();
        this.symptoms = this.repository.getSymptoms();
        this.diagnoses.forEach(diagnosis => {
            this.diagnosesByIndex.set(diagnosis.id, diagnosis);
        });
        this.symptoms.forEach(symptom => {
            this.symptomsByIndex.set(symptom.id, symptom);
        });
    }

}