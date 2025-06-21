class Symptom {
    public id: string;
    public name: string;
}

class SymptomEntry {
    public symptom: Symptom;
    public precense: Presence;
    public comments: string;
}