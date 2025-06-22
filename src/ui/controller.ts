/// <reference path="./component.ts" />
/// <reference path="./new.ts" />
/// <reference path="./notes.ts" />

class Controller {

    private caze: Case;
    private newButtonComponent: NewButtonComponent;
    private notesComponent: NotesComponent;


    public constructor(private engine: Engine) {
        this.engine = engine;
        this.caze = new Case();
        this.newButtonComponent = new NewButtonComponent(this);
        this.notesComponent = new NotesComponent(this.caze);
    }

    public innit(): void {
        this.newButtonComponent.innit();
        this.notesComponent.innit();
    }

    public load(caze: Case): void {
        this.notesComponent.setCase(caze);
    }

}