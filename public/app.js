export const COLLECTION_PATHS = Object.freeze({
    conditions: "./data/conditions.json",
    symptoms: "./data/symptoms.json",
    tests: "./data/tests.json",
    conditionEntries: "./data/condition-entries.json",
    symptomEntries: "./data/symptom-entries.json",
    testEntries: "./data/test-entries.json",
    cases: "./data/cases.json",
    citations: "./data/citations.json"
});

const COLLECTION_KEYS = Object.keys(COLLECTION_PATHS);
const requiredString = (record, key, collection) => {
    if (typeof record[key] !== "string" || !record[key].trim()) {
        throw new Error(`${collection} contains an item without a valid ${key}.`);
    }
};
const ensureReferences = (records, key, ids, collection) => records.forEach(record => {
    if (!Array.isArray(record[key]) && typeof record[key] !== "string") {
        throw new Error(`${collection} contains an item with invalid ${key} references.`);
    }
    const references = Array.isArray(record[key]) ? record[key] : [record[key]];
    references.forEach(reference => {
        if (!ids.has(reference)) throw new Error(`${collection} references missing identifier "${reference}".`);
    });
});

export function validateCollections(collections) {
    COLLECTION_KEYS.forEach(key => {
        if (!Array.isArray(collections[key])) throw new Error(`${key} must be a JSON array.`);
        const ids = new Set();
        collections[key].forEach(record => {
            if (!record || typeof record !== "object") throw new Error(`${key} contains an invalid item.`);
            requiredString(record, "id", key);
            if (ids.has(record.id)) throw new Error(`${key} contains duplicate identifier "${record.id}".`);
            ids.add(record.id);
        });
    });
    const ids = Object.fromEntries(COLLECTION_KEYS.map(key => [key, new Set(collections[key].map(record => record.id))]));
    collections.conditions.forEach(record => {
        requiredString(record, "name", "conditions");
        requiredString(record, "desc", "conditions");
        if (!Number.isInteger(record.priority)) throw new Error("conditions contains an invalid priority.");
        ensureReferences([record], "symptoms", ids.symptoms, "conditions");
        ensureReferences([record], "citation", ids.citations, "conditions");
    });
    collections.symptoms.forEach(record => {
        requiredString(record, "name", "symptoms");
        requiredString(record, "desc", "symptoms");
        ensureReferences([record], "tests", ids.tests, "symptoms");
        ensureReferences([record], "citation", ids.citations, "symptoms");
    });
    collections.tests.forEach(record => {
        requiredString(record, "name", "tests");
        requiredString(record, "desc", "tests");
        ensureReferences([record], "citation", ids.citations, "tests");
    });
    collections.citations.forEach(record => {
        requiredString(record, "bibtex", "citations");
        requiredString(record, "ieee", "citations");
    });
    ensureReferences(collections.conditionEntries, "condition", ids.conditions, "conditionEntries");
    ensureReferences(collections.symptomEntries, "symptom", ids.symptoms, "symptomEntries");
    ensureReferences(collections.testEntries, "test", ids.tests, "testEntries");
    return collections;
}

export async function loadCollections(fetcher = fetch) {
    const entries = await Promise.all(COLLECTION_KEYS.map(async key => {
        const response = await fetcher(COLLECTION_PATHS[key]);
        if (!response.ok) throw new Error(`Could not load ${key} (${response.status}).`);
        try {
            return [key, await response.json()];
        } catch {
            throw new Error(`Could not parse ${key} as JSON.`);
        }
    }));
    return validateCollections(Object.fromEntries(entries));
}

export function rankConditions(conditions, symptoms, findings) {
    const symptomNames = new Map(symptoms.map(symptom => [symptom.id, symptom.name]));
    return conditions.map(condition => {
        const presentMatches = condition.symptoms.filter(id => findings.get(id) === "present");
        const absentMatch = condition.symptoms.some(id => findings.get(id) === "absent");
        return {
            condition,
            score: presentMatches.length,
            matches: presentMatches.map(id => symptomNames.get(id)),
            applicable: !absentMatch
        };
    }).filter(result => result.applicable).sort((left, right) =>
        right.score - left.score ||
        right.condition.priority - left.condition.priority ||
        left.condition.name.localeCompare(right.condition.name, undefined, { sensitivity: "base" }) ||
        left.condition.id.localeCompare(right.condition.id)
    );
}

const elements = {
    loading: document.querySelector("#loading-view"),
    error: document.querySelector("#error-view"),
    errorMessage: document.querySelector("#error-message"),
    retry: document.querySelector("#retry-button"),
    entry: document.querySelector("#entry-view"),
    results: document.querySelector("#results-view"),
    status: document.querySelector("#status"),
    caseForm: document.querySelector("#case-form"),
    description: document.querySelector("#case-description"),
    descriptionError: document.querySelector("#description-error"),
    caseSummary: document.querySelector("#case-summary"),
    symptomList: document.querySelector("#symptom-list"),
    diagnosisList: document.querySelector("#diagnosis-list"),
    matchCount: document.querySelector("#match-count"),
    reset: document.querySelector("#reset-button")
};
let collections;
let activeCase;

function showState(state) {
    elements.loading.hidden = state !== "loading";
    elements.error.hidden = state !== "error";
    elements.entry.hidden = state !== "entry";
    elements.results.hidden = state !== "results";
}
function setStatus(message, tone = "") {
    elements.status.className = `status ${tone}`.trim();
    elements.status.textContent = message;
}
function renderFindings() {
    elements.symptomList.innerHTML = collections.symptoms.map(symptom => {
        const value = activeCase.findings.get(symptom.id) || "unassessed";
        return `<div class="symptom-control">
            <span class="symptom-name">${escapeHtml(symptom.name)}</span>
            <p class="symptom-description">${escapeHtml(symptom.desc)}</p>
            <div class="finding-options">
                ${["present", "absent", "unassessed"].map(option => `
                    <label><input type="radio" name="symptom-${symptom.id}" value="${option}" ${value === option ? "checked" : ""}> ${option === "unassessed" ? "Not assessed" : option[0].toUpperCase() + option.slice(1)}</label>
                `).join("")}
            </div>
        </div>`;
    }).join("");
    elements.symptomList.querySelectorAll("input").forEach(input => input.addEventListener("change", event => {
        activeCase.findings.set(event.target.name.replace("symptom-", ""), event.target.value);
        renderResults();
    }));
}
function renderResults() {
    const ranked = rankConditions(collections.conditions, collections.symptoms, activeCase.findings);
    elements.matchCount.textContent = `${ranked.length} match${ranked.length === 1 ? "" : "es"}`;
    elements.diagnosisList.innerHTML = ranked.length ? ranked.map(result => `
        <article class="condition-card">
            <h3>${escapeHtml(result.condition.name)}</h3>
            <p>${escapeHtml(result.condition.desc)}</p>
            <p class="related-findings"><strong>Related present findings:</strong> ${result.matches.length ? result.matches.map(escapeHtml).join(", ") : "None recorded yet"}</p>
        </article>
    `).join("") : `<div class="no-match"><strong>No matching diagnosis in the loaded data.</strong><br>Revise the symptom findings or start a new case.</div>`;
}
function renderActiveCase() {
    elements.caseSummary.textContent = activeCase.description;
    renderFindings();
    renderResults();
    showState("results");
}
function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, character => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[character]));
}

elements.caseForm.addEventListener("submit", event => {
    event.preventDefault();
    const description = elements.description.value.trim();
    if (!description) {
        elements.descriptionError.hidden = false;
        elements.descriptionError.textContent = "Enter a presentation description before starting the diagnosis.";
        elements.description.focus();
        setStatus("A presentation description is required.", "error");
        return;
    }
    elements.descriptionError.hidden = true;
    activeCase = { description, findings: new Map() };
    setStatus("Case started.", "success");
    renderActiveCase();
});
elements.reset.addEventListener("click", () => {
    activeCase = undefined;
    elements.description.value = "";
    setStatus("");
    showState("entry");
    elements.description.focus();
});
async function initialize() {
    showState("loading");
    setStatus("Loading local diagnosis data.");
    try {
        collections = await loadCollections();
        showState("entry");
        setStatus("Diagnosis data ready.", "success");
    } catch (error) {
        showState("error");
        elements.errorMessage.textContent = `${error.message} Diagnosis results are disabled until valid data is available.`;
        setStatus("Diagnosis data unavailable.", "error");
    }
}
elements.retry.addEventListener("click", initialize);
initialize();

if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => navigator.serviceWorker.register("./service-worker.js").catch(error => {
        console.error("Service worker registration failed:", error);
    }));
}
