import { Exam } from "../database/Exam";

export class DiagnosedExam {

    positive: boolean;
    comments: string;

    constructor(readonly exam: Exam) { }

}