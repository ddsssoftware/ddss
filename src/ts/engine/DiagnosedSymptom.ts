import { Symptom } from "../database/Symptom";

export class DiagnosedSymptom {

    positive: boolean;
    comments: string;

    constructor(readonly symptom: Symptom) { }

}