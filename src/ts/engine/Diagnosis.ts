import { DiagnosedDisease } from "./DiagnosedDisease";
import { DiagnosedExam } from "./DiagnosedExam";
import { DiagnosedSymptom } from "./DiagnosedSymptom";

export class Diagnosis {

    comments: string;

    constructor(readonly diagnosedDiseases: DiagnosedDisease[], readonly diagnosedSymptoms: DiagnosedSymptom[], readonly diagnosedExam: DiagnosedExam[]) { };
}
