import socket

HOST = "192.168.0.37"
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))

while True:
    mensagem = input("Digite uma mensagem: ")
    s.sendall(str.encode(f'{mensagem}')) #codifica na forma de string
    data = s.recv(1024)

    print(f'Mensagem ecoada!, {data.decode()}')