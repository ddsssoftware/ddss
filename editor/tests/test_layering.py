"""Guards on the layer boundaries, so the architecture cannot silently rot.

The checks read each module's own source and look at what it imports, so they
hold whatever the modules happen to do at run time:

- a controller must not reach for the UI framework (it returns results instead),
- a view must not decide rules, read files, or hold the model (it holds a
  controller),
- the model must not reach for the UI framework either.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE = Path(__file__).resolve().parents[1]


def _imports_of(layer: str) -> dict[str, set[str]]:
    """Return, per module in ``layer``, the modules it imports."""
    imported: dict[str, set[str]] = {}
    for path in sorted((PACKAGE / layer).rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                names.add(node.module)
        imported[str(path.relative_to(PACKAGE))] = names
    return imported


CONTROLLERS = _imports_of("controllers")
VIEWS = _imports_of("views")
MODELS = _imports_of("models")

#: A view may show what a controller returned, but must not decide rules, read
#: or write files, or hold the model: those all belong to the layers below it.
VIEWS_MAY_NOT_IMPORT = (
    "editor.models.editor_model",
    "editor.models.repository",
    "editor.models.rules",
)


@pytest.mark.parametrize("module", sorted(CONTROLLERS))
def test_no_controller_imports_textual(module: str) -> None:
    offending = [
        name for name in CONTROLLERS[module] if name.startswith("textual")
    ]

    assert offending == [], f"{module} imports {offending}"


@pytest.mark.parametrize("module", sorted(VIEWS))
def test_no_view_decides_rules_or_touches_the_store(module: str) -> None:
    offending = [
        name for name in VIEWS[module] if name in VIEWS_MAY_NOT_IMPORT
    ]

    assert offending == [], f"{module} imports {offending}"


@pytest.mark.parametrize("module", sorted(MODELS))
def test_no_model_module_imports_textual(module: str) -> None:
    offending = [name for name in MODELS[module] if name.startswith("textual")]

    assert offending == [], f"{module} imports {offending}"
