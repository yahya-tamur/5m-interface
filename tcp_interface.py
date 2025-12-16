import socket

commands = eval(open('commands.json').read())

def send_to_printer(command, ip):
    try:
        s = socket.socket()
        s.set_timeout(0.1)
        s.connect((ip, 8899))
        resp_code = s.send(commands[command].encode('ascii'))
        resp = s.recv(4096)
        s.close()
        return (resp_code, resp)
    except:
        return (503, ''.encode('ascii'))

