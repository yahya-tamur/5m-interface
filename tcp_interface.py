import socket

commands = eval(open('commands.json').read())

def send_to_printer(command, ip):
    s = socket.create_connection((ip, 8899))
    resp_code = s.send(commands[command].encode('ascii'))
    resp = s.recv(4096)
    s.close()

    return (resp_code, resp)
