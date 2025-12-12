import os
import sys

def command_button(command, indent=6):
    indent = ' '*indent
    button = f"""{indent}<button onclick="printer_{command}()"> {command}</button>"""

    script = f"""{indent}<script>printer_{command} = () => $.ajax("{command}").then(content => document.getElementById('resp').innerText = content)</script>\n"""

    return button, script


commands = eval(open('commands.json').read())

schema = open('schema.html').read()

buttons, scripts = "", ""

for c in commands:
    b, s = command_button(c)
    buttons += b + " "
    scripts += s

schema = schema.replace('$#commands#$', buttons + '\n' + scripts)

from env import printer_ip

video = f"""<img id="stream" alt="Camera feed didn't load. You can make sure it's not open elsewhere and refresh this page." src=http://{printer_ip}:8080/?action=stream />"""

schema = schema.replace("$#video#$", video)

open('index.html', 'w').write(schema)
