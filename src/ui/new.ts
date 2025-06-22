class NewButtonComponent extends Component {

    public constructor(private controller: Controller) {
        super("sys__new", null);
    }

    public reset(): void {
        throw new Error("Method not implemented.");
    }

    public innit(): void {
        this.getElement().addEventListener('click', this.onClick.bind(this));
    }

    public onClick() {
        this.controller.load(new Case());
    }

}