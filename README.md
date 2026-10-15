# Differential Diagnosis Support System

For medical professionals only.

The medical information is intended for background reading and general interest. Content is asserted neither complete nor error free.

Please consult your own licensed physician regarding diagnosis and treatment of any medical condition

## Run the client

Start the dependency-free static file server from the repository root:

```sh
python server.py
```

Then open <http://127.0.0.1:8000/> in a browser. The server serves files from
`public/` and supports custom bind settings, for example:

```sh
python server.py --host 0.0.0.0 --port 8080
```

## Run the editor

SSEditor is the terminal application used to maintain the clinical data the
client reads. It lives in `editor/` and edits the collections under
`public/data` directly.

The package is split into three layers. `editor/models/` holds the record
classes, the collection files, the rules and the identifiers; each record class
reads and writes its own fields, and one `Validator` holds every rule.
`editor/controllers/` holds one class per use case, with methods that take values
and return a result. `editor/views/` holds the Textual screens, which render what
a controller returned and own their own navigation.
`editor/README.md` describes the layers and lists every rule with the tests that
cover it.

Install it, with its development dependencies, into the project virtual
environment:

```sh
python3 -m pip --python .venv/bin/python install --upgrade pip
.venv/bin/pip install -e ".[dev]"
```

Then launch it from the repository root:

```sh
.venv/bin/python -m editor
```

The same application is available through the console script installed with the
package:

```sh
.venv/bin/sseditor
```

Keys: `enter` opens the highlighted entity type, `a` adds a record, `e` edits
the highlighted record, `d` deletes it, and `escape` goes back. A write is
refused, with the reason shown on screen, when it would break a data rule.

Run the tests with:

```sh
.venv/bin/python -m pytest
```

Every run reports line and branch coverage for the `editor` package and lists
any uncovered lines. A browsable HTML report can be generated with the
convenience script (written to `coverage/html`):

```sh
editor/run_unit_test.sh
```

Coverage settings such as the measured source, the omission of the test tree,
and the terminal/HTML/XML report destinations live in the `[tool.coverage.*]`
sections of `pyproject.toml`.

## How it works

DDSS maintains database of diseases and its symptoms.

Steps for a diagnosis:

1. Start by describing the case and entering the symptoms presented.
2. Based on the case information DDSS will present a list of possible diagnoses and related symptoms. The list will be sorted by urgency - that is, the diagnoses and symptoms at the top of the list should be dealt first.
3. Indicate which symptoms of the list are present/not present in the case and DDSS will refine the list.
4. If a diagnosis was not reached, go back to step 2.
