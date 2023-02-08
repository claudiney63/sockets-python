import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('localhost', 7777))
server.listen(1)

con, end = server.accept()

namefile = con.recv(1024).decode()

with open(namefile, 'rb') as file:
    for data in file.readlines():
        con.send(data)

    print('Arquivo enviado!')