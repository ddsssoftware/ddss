"""The view layer: the Textual screens.

A view composes widgets, calls one controller method per event, renders the value
it gets back, and owns its own navigation. It never decides a rule and never
touches a file.
"""

from editor.views.detail import EntityDetailView, field_widget_id
from editor.views.home import HomeView
from editor.views.list import EntityListView, RecordItem

__all__ = [
    "EntityDetailView",
    "EntityListView",
    "HomeView",
    "RecordItem",
    "field_widget_id",
]
