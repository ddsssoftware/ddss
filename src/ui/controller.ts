/// <reference path="./component.ts" />
/// <reference path="./notes.ts" />

class Controller {

    private caze: Case;
    private notesComponents: NotesComponent;

    public constructor(private engine: Engine) {
        this.engine = engine;
        this.caze = new Case();
        this.notesComponents = new NotesComponent(this.caze);
    }

    public innit(): void {
        this.notesComponents.innit();
    }

}