# Differential Diagnosis Support System

For medical professionals only.

The medical information is intended for background reading and general interest. Content is asserted neither complete nor error free.

Please consult your own licensed physician regarding diagnosis and treatment of any medical condition

## How to install

* Download this repository

* Serve the `public` folder using your favorite web server and user your browser to use the application. For example, using php's embedded server

```bash
php -S localhost:8080 -t ./public
```

## Contributing

### Typescript

Simply call the `tsc` compiler at the project's root folder. It will compile the source at `src` folder and place it and `public\js` ready for use.

### Medical Knowledge

Edit the files `public\data\diagnoses.json` and `public\data\symptoms.json`