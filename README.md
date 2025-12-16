## Usage:

* Set your printer's ip address in env.py

* Run `python server.py`

* Connect to the server address (default `localhost:8080/?printer-ip=<your printer's ip address>`) from any browser. This even works if you enter this address where you would usually enter the camera feed in orca slicer (screenshot below).

Note that you need to click the 'resume' button on the printer if you press 'pause'.
## Organization:

`schema.html` and `index.css` describe the web page.

`make_index.py` creates `index.html` from the schema.
(In practice, this just adds the video and buttons programatically).

`commands.json` lists gcode M-commands that will be turned into buttons to
send the corresponding command to the printer. You can add or remove buttons
by editing this, re-running `make_index.py`, and restarting the server.

`tcp_interface.py` has the code to connect to the printer.

`server.py` has the server which serves the web page, and connects to the
printer when the command buttons are clicked.

## Screenshot:

![screenshot](./screenshot2.png)

## To Do:

* Format printer output more nicely?
* Functionality to monitor every 5s or something?
* Improve website look
