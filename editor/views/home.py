"""The home view: choose which entity type to edit."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, OptionList, Static
from textual.widgets.option_list import Option

from editor.controllers.home import HomeController
from editor.views.list import EntityListView


class HomeView(Screen[None]):
    """Offer the editable entity types."""

    BINDINGS = [("escape", "app.quit", "Quit")]

    def __init__(self, controller: HomeController) -> None:
        super().__init__()
        self.controller = controller

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Choose an entity type", id="home-title")
        yield OptionList(
            *(
                Option(label, id=entity_type)
                for entity_type, label in self.controller.menu()
            ),
            id="entity-types",
        )
        yield Footer()

    def on_option_list_option_selected(
        self, event: OptionList.OptionSelected
    ) -> None:
        """Open the list view for the chosen entity type."""
        self.app.push_screen(
            EntityListView(self.controller.open(str(event.option.id)))
        )


__all__ = ["HomeView"]
