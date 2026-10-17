"""The screen that attaches stored records to a reference field."""

from __future__ import annotations

from collections.abc import Sequence

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    SelectionList,
    Static,
)

from editor.controllers.entity_detail import EntityDetailController, ReferenceChoice


class ReferencePickerView(Screen[list[str] | None]):
    """Choose one or more stored records to attach.

    Dismisses with the chosen identifiers, or ``None`` when cancelled. The
    search term narrows the offered records by name or alternative name.
    """

    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(
        self,
        controller: EntityDetailController,
        field_name: str,
        title: str,
        attached: Sequence[str] = (),
    ) -> None:
        super().__init__()
        self.controller = controller
        self.field_name = field_name
        self.title_text = title
        self.attached = tuple(attached)
        self.chosen: set[str] = set()
        self._choices: list[ReferenceChoice] = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(self.title_text, id="picker-title")
        yield Input(placeholder="Search", id="picker-search")
        yield Static("", id="picker-status")
        yield SelectionList(id="picker-options")
        with Horizontal(id="picker-actions"):
            yield Button("Attach", id="attach", variant="primary")
            yield Button("Cancel", id="cancel")
        yield Footer()

    def on_mount(self) -> None:
        self.refresh_options()

    # -- rendering ----------------------------------------------------------

    def refresh_options(self) -> None:
        """Rebuild the offered records for the current search term."""
        self._keep_visible_selections()
        term = self.query_one("#picker-search", Input).value
        self._choices = self.controller.available_references(
            self.field_name,
            term,
            self.attached,
        )
        options = self.query_one("#picker-options", SelectionList)
        options.clear_options()
        for choice in self._choices:
            options.add_option((choice.label, choice.identifier))
        for choice in self._choices:
            if choice.identifier in self.chosen:
                options.select(choice.identifier)
        self.query_one("#picker-status", Static).update(self._status(term))

    def _status(self, term: str) -> str:
        """Return the message shown under the search box."""
        if self._choices:
            return ""
        if term.strip():
            return "No matching records."
        return "No records available to attach."

    def _keep_visible_selections(self) -> None:
        """Fold the visible ticks into ``chosen`` before the options rebuild."""
        options = self.query_one("#picker-options", SelectionList)
        visible = {choice.identifier for choice in self._choices}
        self.chosen -= visible
        self.chosen |= set(options.selected)

    # -- values -------------------------------------------------------------

    def chosen_identifiers(self) -> list[str]:
        """Return the identifiers to attach, in the order they are offered."""
        options = self.query_one("#picker-options", SelectionList)
        visible = {choice.identifier for choice in self._choices}
        chosen = (self.chosen - visible) | set(options.selected)
        return [
            choice.identifier
            for choice in self.controller.available_references(
                self.field_name,
                "",
                self.attached,
            )
            if choice.identifier in chosen
        ]

    # -- actions ------------------------------------------------------------

    def action_attach(self) -> None:
        """Attach the ticked records and close."""
        self.dismiss(self.chosen_identifiers())

    def action_cancel(self) -> None:
        """Close without attaching anything."""
        self.dismiss(None)

    def on_input_changed(self, event: Input.Changed) -> None:
        self.refresh_options()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "attach":
            self.action_attach()
        elif event.button.id == "cancel":
            self.action_cancel()


__all__ = ["ReferencePickerView"]
