import os
import sys
from env import printer_ip

commands = eval(open('commands.json').read())

schema = open('schema.html').read()

buttons_html = ""
indent = ' '*4

for command in commands:
    buttons_html += f"""{indent}<button onclick="printer_{command}()"> {command}</button>\n"""
    buttons_html += f"""{indent}<script>printer_{command} = () => $.ajax("{command}").then(content => document.getElementById('resp').innerText = content)</script>\n"""

schema = schema.replace('$#commands#$', buttons_html)

video = f"""{indent}<img id="stream" alt="Camera feed didn't load. You can make sure it's not open elsewhere and refresh this page." src=http://{printer_ip}:8080/?action=stream />"""

schema = schema.replace("$#video#$", video)

open('index.html', 'w').write(schema)
