class Case {
    public notes: string;
    public symptoms: SymptomEntry[];
    public diagnosis: DiagnosisEntry[];
}

enum Presence {
    Present = "Present",
    NotPresent = "Not Present",
    Unknown = "Unknown"
}