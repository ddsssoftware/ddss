"""The detail view: add or edit one record of one entity type."""

from __future__ import annotations

from collections.abc import Sequence

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
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

from editor.controllers.entity_detail import AttachedReference, EntityDetailController
from editor.models.fields import FieldSpec, label_of, spec_for
from editor.views.picker import ReferencePickerView

UNKNOWN_REFERENCE = "Unknown"


def field_widget_id(field_spec: FieldSpec) -> str:
    """Return the widget id used for one field's editor."""
    return f"field-{field_spec.name}"


def reference_table_id(field_spec: FieldSpec) -> str:
    """Return the widget id used for one reference field's table."""
    return f"references-{field_spec.name}"


class ReferenceRow(Horizontal):
    """One attached reference, with its name, identifier and row actions."""

    def __init__(self, reference: AttachedReference, field_name: str) -> None:
        super().__init__(classes="reference-row")
        self.identifier = reference.identifier
        self.field_name = field_name
        self.label = self._label_of(reference)
        self.available = reference.record is not None

    @staticmethod
    def _label_of(reference: AttachedReference) -> str:
        """Return the name a reference row shows for one stored reference."""
        if reference.record is None:
            return UNKNOWN_REFERENCE
        return label_of(reference.record)

    def compose(self) -> ComposeResult:
        yield Label(self.label, classes="reference-name")
        yield Label(self.identifier, classes="reference-id")
        yield Button(
            "Go to",
            classes="reference-goto",
            disabled=not self.available,
        )
        yield Button("Remove", classes="reference-remove")

    def show_reference(self, label: str, available: bool) -> None:
        """Show a re-resolved name and whether the row can still be opened."""
        self.label = label
        self.available = available
        self.query_one(".reference-name", Label).update(label)
        self.query_one(".reference-goto", Button).disabled = not available


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
                if field_spec.kind == "reference_list":
                    with Vertical(
                        id=reference_table_id(field_spec),
                        classes="reference-table",
                    ):
                        for reference in self.controller.attached_references(
                            field_spec.name
                        ):
                            yield ReferenceRow(reference, field_spec.name)
                    yield Button(
                        f"Add {self._target_label(field_spec)}",
                        id=f"add-{field_spec.name}",
                        classes="reference-add",
                    )
                else:
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

    @staticmethod
    def _target_label(field_spec: FieldSpec) -> str:
        """Return the entity label the field points at."""
        if field_spec.target is None:
            return "Record"
        return spec_for(field_spec.target).label

    # -- rendering ----------------------------------------------------------

    def reference_rows(self, field_name: str) -> list[ReferenceRow]:
        """Return the reference rows currently shown for one field."""
        table = self.query_one(f"#references-{field_name}", Vertical)
        return [
            child for child in table.children if isinstance(child, ReferenceRow)
        ]

    def reference_identifiers(self, field_name: str) -> list[str]:
        """Return the identifiers currently attached for one field."""
        return [row.identifier for row in self.reference_rows(field_name)]

    # -- rendering ----------------------------------------------------------

    def values(self) -> dict[str, str | list[str]]:
        """Return the current text of every field the form shows."""
        return {
            field_spec.name: self._widget_value(field_spec)
            for field_spec in self.controller.spec.fields
        }

    def _widget_value(self, field_spec: FieldSpec) -> str | list[str]:
        """Read the current value from one field's editor widget."""
        if field_spec.kind == "reference_list":
            return self.reference_identifiers(field_spec.name)
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
        button = event.button
        if button.id == "save":
            self.action_save()
        elif button.id == "cancel":
            self.action_cancel()
        elif button.has_class("reference-add"):
            field_name = button.id.removeprefix("add-") if button.id else ""
            self.open_reference_picker(field_name)
        elif button.has_class("reference-remove"):
            row = button.parent
            if isinstance(row, ReferenceRow):
                row.remove()
        elif button.has_class("reference-goto"):
            row = button.parent
            if isinstance(row, ReferenceRow):
                self.open_reference(row)

    def open_reference_picker(self, field_name: str) -> None:
        """Open the chooser for one reference field."""
        field_spec = next(
            field for field in self.controller.spec.fields if field.name == field_name
        )
        self.app.push_screen(
            ReferencePickerView(
                self.controller,
                field_name,
                title=f"Attach {self._target_label(field_spec)}",
                attached=self.reference_identifiers(field_name),
            ),
            callback=lambda identifiers: self.attach_references(
                field_name, identifiers
            ),
        )

    def attach_references(
        self, field_name: str, identifiers: Sequence[str] | None
    ) -> None:
        """Append the picker's records to one reference table."""
        if not identifiers:
            return
        table = self.query_one(f"#references-{field_name}", Vertical)
        for identifier in identifiers:
            record = self.controller.lookup_reference(field_name, identifier)
            table.mount(ReferenceRow(AttachedReference(identifier, record), field_name))

    def open_reference(self, row: ReferenceRow) -> None:
        """Open the record one attached reference points at."""
        record = self.controller.lookup_reference(row.field_name, row.identifier)
        if record is None:
            return
        target = EntityDetailController(
            self.controller.model,
            record.ENTITY_TYPE,
            record,
        )
        self.app.push_screen(
            EntityDetailView(target),
            callback=lambda saved: self.refresh_reference_labels(row.field_name),
        )

    def refresh_reference_labels(self, field_name: str) -> None:
        """Re-resolve the rows' names after a referenced record may have changed."""
        for row in self.reference_rows(field_name):
            record = self.controller.lookup_reference(field_name, row.identifier)
            row.show_reference(
                label_of(record) if record is not None else UNKNOWN_REFERENCE,
                record is not None,
            )


__all__ = [
    "EntityDetailView",
    "ReferenceRow",
    "field_widget_id",
    "reference_table_id",
]
