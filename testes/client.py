from socket import *
from threading import Thread

HOST = "192.168.0.37"
PORT = 50000

print(f"HOST: {HOST} PORT: {PORT}")

clie = socket(AF_INET, SOCK_STREAM) # AF_INET = IPV4 | SOCK_STREAM = TCP
clie.connect((HOST, PORT)) # conecta ao servidor

def enviar():
    while True:
        data = input("Digite algo: ")

        if data == 'Exit':
            print('Fechando conexao...')
            clie.close()
            break

        data = f'{data}'
        clie.send(data.encode("utf-8")) # envia a mensagem codificada em bits

def receber():
    while True:
        data = clie.recv(1024) # 1024 = tamanho do buffer
        print(f'Mensagem Recebida: {data.decode("utf-8")}') # decodifica a mensagem pq vem em bits
        

Thread(target=enviar).start()
Thread(target=receber).start()
