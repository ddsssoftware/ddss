"""The detail view: add or edit one record of one entity type."""

from __future__ import annotations

from collections.abc import Sequence

from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    Static,
    TextArea,
)

from editor.controllers.entity_detail import EntityDetailController
from editor.models.fields import FieldSpec


def field_widget_id(field_spec: FieldSpec) -> str:
    """Return the widget id used for one field's editor."""
    return f"field-{field_spec.name}"


class EntityDetailView(Screen[bool]):
    """Add or edit a record, showing the rules' violations when it cannot save.

    Dismisses with ``True`` when the record was stored and ``False`` when the
    administrator left without saving.
    """

    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, controller: EntityDetailController) -> None:
        super().__init__()
        self.controller = controller

    def compose(self) -> ComposeResult:
        yield Header()
        values = self.controller.initial_values()
        with VerticalScroll(id="form"):
            yield Static(self._title(), id="detail-title")
            yield Static("", id="violations")
            for field_spec in self.controller.spec.fields:
                yield Label(field_spec.label, id=f"label-{field_spec.name}")
                yield self._field_widget(field_spec, values[field_spec.name])
        with Horizontal(id="actions"):
            yield Button("Save", id="save", variant="primary")
            yield Button("Cancel", id="cancel")
        yield Footer()

    def _title(self) -> str:
        """Return the heading for the form."""
        action = "Add" if self.controller.is_new else "Edit"
        return f"{action} {self.controller.spec.label}"

    def _field_widget(self, field_spec: FieldSpec, value: str) -> Input | TextArea:
        """Build the editor widget for one field.

        Free-text fields hold multiline content, so they use a ``TextArea`` and
        keep embedded newlines; every other field stays a single-line ``Input``.
        """
        widget_id = field_widget_id(field_spec)
        if field_spec.kind == "long_text":
            return TextArea(value, id=widget_id)
        return Input(value=value, id=widget_id)

    # -- rendering ----------------------------------------------------------

    def values(self) -> dict[str, str]:
        """Return the current text of every field the form shows."""
        return {
            field_spec.name: self._widget_value(field_spec)
            for field_spec in self.controller.spec.fields
        }

    def _widget_value(self, field_spec: FieldSpec) -> str:
        """Read the current text from one field's editor widget."""
        widget_id = field_widget_id(field_spec)
        if field_spec.kind == "long_text":
            return self.query_one(f"#{widget_id}", TextArea).text
        return self.query_one(f"#{widget_id}", Input).value

    def show_violations(self, messages: Sequence[str]) -> None:
        """Show why the record could not be stored."""
        self.query_one("#violations", Static).update("\n".join(messages))

    # -- actions ------------------------------------------------------------

    def action_save(self) -> None:
        """Store the form's values, or stay open and show what is wrong."""
        violations = self.controller.save(self.values())
        if violations:
            self.show_violations(
                [violation.message for violation in violations]
            )
            return
        self.dismiss(True)

    def action_cancel(self) -> None:
        """Leave without storing anything."""
        self.dismiss(False)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self.action_save()
        elif event.button.id == "cancel":
            self.action_cancel()


__all__ = [
    "EntityDetailView",
    "field_widget_id",
]
