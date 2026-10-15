"""The list view: list, search, add, edit and delete one entity type."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    Static,
)

from editor.controllers.entity_list import EntityListController
from editor.models.records import Record
from editor.views.detail import EntityDetailView


class RecordItem(ListItem):
    """A record row that carries the record it represents."""

    def __init__(self, record: Record, label: str) -> None:
        super().__init__(Label(label))
        self.record = record
        self.label_text = label


class EntityListView(Screen[None]):
    """List one entity type, and act on the highlighted record."""

    BINDINGS = [
        ("a", "add", "Add"),
        ("e", "edit", "Edit"),
        ("d", "delete", "Delete"),
        ("escape", "close", "Back"),
    ]

    def __init__(self, controller: EntityListController) -> None:
        super().__init__()
        self.controller = controller

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Search", id="search")
        yield Static("", id="status")
        yield ListView(id="records")
        with Horizontal(id="list-actions"):
            yield Button("Add", id="add", variant="primary")
            yield Button("Edit", id="edit")
            yield Button("Delete", id="delete")
        yield Footer()

    def on_mount(self) -> None:
        self.refresh_records()
        error = self.controller.load_error()
        if error:
            self.show_status(error)

    # -- rendering ----------------------------------------------------------

    def refresh_records(self) -> None:
        """Rebuild the list from the controller's records and the search term."""
        term = self.query_one("#search", Input).value
        view = self.query_one("#records", ListView)
        view.clear()
        for record in self.controller.items(term):
            view.append(RecordItem(record, self.controller.label_for(record)))

    def show_status(self, message: str) -> None:
        """Show a message to the administrator."""
        self.query_one("#status", Static).update(message)

    def visible_labels(self) -> list[str]:
        """Return the labels currently listed, in order."""
        view = self.query_one("#records", ListView)
        return [
            child.label_text
            for child in view.children
            if isinstance(child, RecordItem)
        ]

    def selected_record(self) -> Record | None:
        """Return the highlighted record, if any."""
        view = self.query_one("#records", ListView)
        child = view.highlighted_child
        return child.record if isinstance(child, RecordItem) else None

    def on_input_changed(self, event: Input.Changed) -> None:
        self.refresh_records()

    # -- actions ------------------------------------------------------------

    def action_add(self) -> None:
        """Open a blank detail view."""
        self.open_detail(None)

    def action_edit(self) -> None:
        """Open the highlighted record for editing."""
        record = self.selected_record()
        if record is None:
            self.show_status("Select a record to edit.")
            return
        self.open_detail(record)

    def open_detail(self, record: Record | None) -> None:
        """Push the detail view for adding, or for editing ``record``."""
        self.app.push_screen(
            EntityDetailView(self.controller.detail_controller(record)),
            callback=self.after_detail,
        )

    def after_detail(self, saved: bool | None) -> None:
        """Reload the list and report what happened."""
        if not saved:
            return
        self.controller.refresh()
        error = self.controller.load_error()
        if error:
            self.show_status(error)
            return
        self.refresh_records()
        self.show_status("Saved.")

    def action_delete(self) -> None:
        """Delete the highlighted record unless something references it."""
        record = self.selected_record()
        if record is None:
            self.show_status("Select a record to delete.")
            return
        violations = self.controller.delete(record)
        if violations:
            self.show_status(violations[0].message)
            return
        deleted = record.id
        self.controller.refresh()
        self.refresh_records()
        self.show_status(f"Deleted {deleted}.")

    def action_close(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add":
            self.action_add()
        elif event.button.id == "edit":
            self.action_edit()
        elif event.button.id == "delete":
            self.action_delete()


__all__ = ["EntityListView", "RecordItem"]
