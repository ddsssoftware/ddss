class Symptom {
    public id: string;
    public name: string;
}

class SymptomEntry {
    public symptom: Symptom;
    public presence: Presence;
    public comments: string;
}