# Differential Diagnosis Support System

For medical professionals only.

The medical information is intended for background reading and general interest. Content is asserted neither complete nor error free.

Please consult your own licensed physician regarding diagnosis and treatment of any medical condition

## How it works

DDSS maintains database of diseases and its symptomns.

Steps for a diagnosis:
1. Start by describing the case and entering the symptomns presented.
2. Based on the case information DDSS will present a list of possible diagnoses and related symptomns. The list will be sorted by urgency - that is, the diagnoses and symptomns at the top of the list should be dealt first.
3. Indicate which symptomns of the list are present/not present in the case and DDSS will refine the list.
4. If a diagnosis was not reached, go back to step 2.

## How to install

* Download this repository

* Serve the `public` folder using your favorite web server and use your browser to open the application. For example, using php's embedded server:
```bash
php -S localhost:8080 -t ./public
```

## Contributing

### Typescript

Simply call the `tsc` compiler at the project's root folder. It will compile the source at `src` folder and place it in `public\js` ready for use.

### Medical Knowledge

The preferred way is to edit using the editor. You need PHP installed, then start the server using
```bash
php -S localhost:7070 -t ./editor
```
Then open your browser and open page http://localhost:7070

You may also edit the files `public\data\diagnoses.json` and `public\data\symptoms.json` directly.