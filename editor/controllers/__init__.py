"""The controller layer.

Each class owns one use case. A controller's methods take values and return the
result, and no controller imports Textual: the view calls one method, gets a
result back, and renders it.
"""

from editor.controllers.entity_detail import EntityDetailController
from editor.controllers.entity_list import EntityListController
from editor.controllers.home import HomeController

__all__ = [
    "EntityDetailController",
    "EntityListController",
    "HomeController",
]
