/// <reference path="./data/symptom.ts" />
/// <reference path="./data/diagnosis.ts" />
/// <reference path="./data/case.ts" />
/// <reference path="./data/repository.ts" />
/// <reference path="./engine/engine.ts" />
/// <reference path="./ui/controller.ts" />

let engine: Engine = new Engine(new Repository());
let controller: Controller = new Controller(engine);

console.log("DDSS ready");