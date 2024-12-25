import { Disease } from "../database/Disease";

export class DiagnosedDisease {

    positive: boolean;
    comments: string;

    constructor(readonly disease: Disease) { }

}