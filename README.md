## Usage:

* Set device UI in orca slicer to `localhost:8080/?printer-ip=<your printer's ip address>`

* Click `run.bat`. This doesn't install anything; it needs to be turned on whenever
    you want to see this ui.

## Organization:

This folder contains the python code that serves the website (using http.server)
and connects to the printer.

The website is mainly on `website/index.html` and `website/update.js`.

I only use npm to make a bundle to include `material-web` and to format files.

To customize theme:

    - Go to `material-web.dev`
    - Click the palette icon on the top right
    - Customize the theme
    - Click the `copy` icon next to `theme controls`
    - Paste into `theme.css` under the `website` folder.

A roboto font file and style sheet is also included so that the font works
offline. It's taken from google fonts.

## Screenshot:

This is for the old version! todo: update

![screenshot](./screenshot2.png)

## To Do:

* use and see if it needs small changes

* time started and time remaining?
        - I'm not sure where or if the printer returns this information, so
        this isn't easy top implement.

