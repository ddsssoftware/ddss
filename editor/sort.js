console.log("Sorting started");

const SYMPTONS_FILE_PATH = '../../../public/data/symptoms.json';
const DIAGNOSES_FILE_PATH = '../../../public/data/diagnoses.json';

const fs = require('fs');

const symptoms = require(SYMPTONS_FILE_PATH);
const diagnoses = require(DIAGNOSES_FILE_PATH);

symptoms.sort((a, b) => ('' + a.id).localeCompare('' + b.id));
diagnoses.sort((a, b) => ('' + a.icd).localeCompare('' + b.icd));
diagnoses.forEach(d => {
    d.symptoms.sort((a, b) => ('' + a).localeCompare('' + b));
});

fs.writeFileSync(SYMPTONS_FILE_PATH, JSON.stringify(symptoms, null, 4));
fs.writeFileSync(DIAGNOSES_FILE_PATH, JSON.stringify(diagnoses, null, 4));

console.log("Sorting ended");