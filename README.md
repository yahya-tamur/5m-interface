## Usage:

* Set your printer's ip address in env.py

* Run

```python server.py```

* Connect to the server address (default `localhost:8080`) from a browser.

Note that you need to click the 'resume' button on the printer if you press 'pause'.
## Organization:

`schema.html` and `index.css` describe the web page.

Run `python make_index.py` to create the `index.html` page from the schema.
(In practice, this just adds the video and buttons programatically).

`commands.json` lists gcode M-commands that will be turned into buttons to
send the corresponding command to the printer. You can add or remove buttons
here.

`tcp_interface.py` has the code to connect to the printer.

`server.py` has the server which serves the web page, and connects to the
printer when the command buttons are clicked.

## Screenshot:

to do.

## To Do:

* Format printer output more nicely?
* Functionality to monitor every 5s or something?
* Improve website look
