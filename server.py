import socket
from threading import *

HOST = '192.168.0.37'
PORT = 50000

print(f"HOST: {HOST} PORT: {PORT}")

# usando ipv4 e TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)

print('Aguardando conexao...')

def server_connection():
    while True:
        conn, adress = s.accept()

        print(f'Conectado em: {adress}')
        while True:
            data = conn.recv(1024)
            if not data:
                print('Fechando conexao...')
                conn.close()
                break
            conn.sendall(data)  # retornando a mensagem para o cliente
            print(f'Mensagem ecoada!, {data.decode()}')

for _ in range(4):
    t = Thread(target=server_connection)
    t.start()
