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

## How it works

DDSS maintains database of diseases and its symptoms.

Steps for a diagnosis:
1. Start by describing the case and entering the symptoms presented.
2. Based on the case information DDSS will present a list of possible diagnoses and related symptoms. The list will be sorted by urgency - that is, the diagnoses and symptoms at the top of the list should be dealt first.
3. Indicate which symptoms of the list are present/not present in the case and DDSS will refine the list.
4. If a diagnosis was not reached, go back to step 2.