/// <reference path="./data/symptom.ts" />
/// <reference path="./data/diagnosis.ts" />
/// <reference path="./data/case.ts" />
/// <reference path="./data/repository.ts" />
/// <reference path="./engine/engine.ts" />
/// <reference path="./ui/controller.ts" />

document.addEventListener('DOMContentLoaded', () => {
    const engine: Engine = new Engine(new Repository());
    const controller: Controller = new Controller(engine);
    controller.innit();
    console.log("DDSS ready");
});

