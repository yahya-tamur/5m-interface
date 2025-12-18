import socket

commands = eval(open("commands.json").read())


def send_to_printer(command, ip):
    try:
        s = socket.create_connection((ip, 8899))
        s.settimeout(1)
        s.send(commands[command].encode("ascii"))
        resp = s.recv(4096)
        s.close()
        return (200, resp)
    except:
        return (503, "".encode("ascii"))
