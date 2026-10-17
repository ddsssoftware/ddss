"""Listing, searching and deleting the records of one entity type."""

from __future__ import annotations

from editor.controllers.entity_detail import EntityDetailController
from editor.controllers.matching import matches
from editor.models.editor_model import EditorModel
from editor.models.records import Record
from editor.models.rules import Violation


class EntityListController:
    """The records of one entity type, and the actions on them."""

    def __init__(self, model: EditorModel, entity_type: str) -> None:
        self.model = model
        self.entity_type = entity_type
        self.spec = model.spec_for(entity_type)

    def items(self, term: str = "") -> list[Record]:
        """Return the records matching ``term`` by name or alternative name."""
        return [record for record in self.records() if matches(record, term)]

    def records(self) -> list[Record]:
        """Return every stored record of this controller's entity type."""
        if self.entity_type == "conditions":
            return self.model.conditions()
        if self.entity_type == "symptoms":
            return self.model.symptoms()
        if self.entity_type == "tests":
            return self.model.tests()
        return self.model.citations()

    def label_for(self, record: Record) -> str:
        """Return the text that names one record in the list."""
        return self.model.label_for(record)

    def detail_controller(self, record: Record | None) -> EntityDetailController:
        """Return a controller for adding, or for editing ``record``."""
        return EntityDetailController(self.model, self.entity_type, record)

    def delete(self, record: Record) -> list[Violation]:
        """Delete ``record`` unless another record still references it.

        An empty list means the record was deleted; otherwise nothing was.
        """
        return self.model.delete(record)

    def refresh(self) -> None:
        """Re-read the collections, so the list shows what is stored now."""
        self.model.reload()

    def load_error(self) -> str | None:
        """Return the problem the model had reading a collection, if any."""
        return self.model.load_error


__all__ = ["EntityListController"]
