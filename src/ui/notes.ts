class NotesComponent extends Component {

    public constructor(caze: Case, controller: Controller) {
        super("case__notes", caze, controller);
    }

    public innit(): void {
        this.getElement().addEventListener('input', this.onInput.bind(this));
    }

    public reset(): void {
        (this.getElement() as HTMLInputElement).value = this.caze.notes;
    }

    public onInput(event: Event): void {
        const target = event.target as HTMLInputElement;
        this.caze.notes = target.value;
    }

}