abstract class Component {

    public constructor(protected id: string, protected caze: Case, protected controller: Controller) { }


    public getElement(): HTMLElement {
        return document.getElementById(this.id);
    }

    public abstract reset(): void;

    public abstract innit(): void;
}