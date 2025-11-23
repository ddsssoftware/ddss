class NewButtonComponent extends Component {

    public constructor(caze: Case, controller: Controller) {
        super("sys__new", caze, controller);
    }

    public reset(): void {
        throw new Error("Method not implemented.");
    }

    public innit(): void {
        this.getElement().addEventListener('click', this.onClick.bind(this));
    }

    public onClick() {
        throw new Error("Method not implemented.");
    }

}