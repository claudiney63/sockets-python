import socket

HOST = '127.0.0.1'
PORT = 50000

#Ipv4 e TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))

s.sendall(str.encode('Bom dia a todos!')) #codifica na forma de string

data = s.recv(1024)

print(f'Mensagem ecoada!, {data.decode()}')