class SymptomsSearchComponent extends Component {

    public constructor(controller: Controller) {
        super("symptoms__input_search", controller);
    }

    public reset(): void {
        throw new Error("Method not implemented.");
    }

    public innit(): void {
        this.getElement().addEventListener('input', this.onInput.bind(this));
    }

    public onInput() {

    }

}