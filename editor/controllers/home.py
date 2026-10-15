"""Choosing which entity type to edit."""

from __future__ import annotations

from editor.controllers.entity_list import EntityListController
from editor.models.editor_model import EditorModel
from editor.models.records import ENTITY_TYPES


class HomeController:
    """The menu of editable entity types."""

    def __init__(self, model: EditorModel) -> None:
        self.model = model

    def menu(self) -> list[tuple[str, str]]:
        """Return ``(entity type, label)`` for every editable type, in order."""
        return [
            (entity_type, self.model.spec_for(entity_type).label)
            for entity_type in ENTITY_TYPES
        ]

    def open(self, entity_type: str) -> EntityListController:
        """Return the controller for listing ``entity_type``."""
        return EntityListController(self.model, entity_type)


__all__ = ["HomeController"]
