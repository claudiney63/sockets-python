from socket import *
from threading import Thread

HOST = "192.168.0.37"
PORT = 50000

print(f"HOST: {HOST} PORT: {PORT}")

clie = socket(AF_INET, SOCK_STREAM) # AF_INET = IPV4 | SOCK_STREAM = TCP
clie.connect((HOST, PORT)) # conecta ao servidor

def enviar():
    while True:
        mensagem = input("Digite algo: ")
        clie.sendall(mensagem.encode("utf-8")) # envia a mensagem codificada em bits

def receber():
    while True:
        data = clie.recv(1024) # 1024 = tamanho do buffer
        print(data.decode("utf-8")) # decodifica a mensagem pq vem em bits

Thread(target=enviar).start()
Thread(target=receber).start()

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# s.connect((HOST, PORT))

# while True:
#     mensagem = input("Digite uma mensagem: ")
#     s.sendall(str.encode(f'{mensagem}')) #codifica na forma de string
#     data = s.recv(1024)

#     print(f'Mensagem ecoada!, {data.decode()}')