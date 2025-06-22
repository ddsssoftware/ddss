class Case {
    public notes: string = '';
    public symptoms: SymptomEntry[];
    public diagnosis: DiagnosisEntry[];

    public getPresentSymptoms(): Symptom[] {
        return this.getSymptomsByPresence(Presence.Present);
    }

    public getSymptomsByPresence(presence: Presence) {
        return this.symptoms.filter(symptomEntry => {
            return symptomEntry.presence == presence;
        }).map(symptomEntry => {
            return symptomEntry.symptom;
        });
    }
}

enum Presence {
    Present = "Present",
    NotPresent = "Not Present",
    Unknown = "Unknown"
}