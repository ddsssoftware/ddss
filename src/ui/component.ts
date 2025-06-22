abstract class Component {

    public constructor(protected id: string, protected caze: Case) { }

    public setCase(caze: Case): void {
        this.caze = caze;
    }

    public getElement(): HTMLElement {
        return document.getElementById(this.id);
    }

    public abstract reset(): void;

    public abstract innit(): void;
}