"""The Textual application: the composition root and the router.

It builds the repository and the model, pushes the first view, and holds the
application CSS. It decides nothing about records, rules or files.
"""

from __future__ import annotations

from pathlib import Path

from textual.app import App

from editor.controllers.entity_list import EntityListController
from editor.controllers.home import HomeController
from editor.models.editor_model import EditorModel
from editor.models.repository import CollectionRepository
from editor.views.home import HomeView
from editor.views.list import EntityListView


class EditorApp(App[None]):
    """Terminal application for editing the DDSS data."""

    TITLE = "Editor"
    SUB_TITLE = "Differential Diagnosis Support System Data Editor"

    CSS = """
    #list-actions { height: auto; }
    #actions { height: auto; }
    #violations { color: $error; }
    #status { height: auto; }
    #form TextArea { height: 8; }
    """

    def __init__(
        self,
        data_directory: Path | None = None,
        initial_entity_type: str | None = None,
    ) -> None:
        super().__init__()
        self.data_directory = data_directory
        self.initial_entity_type = initial_entity_type

    def on_mount(self) -> None:
        """Build the model and open the first view."""
        model = EditorModel(CollectionRepository(self.data_directory))
        if self.initial_entity_type:
            self.push_screen(
                EntityListView(
                    EntityListController(model, self.initial_entity_type)
                )
            )
        else:
            self.push_screen(HomeView(HomeController(model)))


__all__ = ["EditorApp"]
