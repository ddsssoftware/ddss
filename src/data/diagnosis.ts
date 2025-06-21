class Diagnosis {
    public id: string;
    public name: string;
    public criticality: number;
    public symptoms: Symptom[];
}

class DiagnosisEntry {
    public diagnosis: Diagnosis;
    public presence: Presence;
    public comments: string;
}