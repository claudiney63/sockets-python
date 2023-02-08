import socket
from threading import *

lista_de_conn = []
lista_de_adress = []

HOST = '192.168.0.37'
PORT = 50000

print(f"HOST: {HOST} PORT: {PORT}")

# usando ipv4 e TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)

print('Aguardando conexao...')

ip = socket.gethostbyname(socket.gethostname())
print(f"IP: {ip}")

def enviar_mensagem():
    while True:
        data = input("Envie uma mensagem: ")

        data = data.encode()

        for cada_conn in range(len(lista_de_conn)):
                lista_de_conn[cada_conn].sendto(data, lista_de_adress[cada_conn])

def server_connection():
    while True:
        conn, adress = s.accept()

        global lista_de_adress

        lista_de_conn.append(conn)
        lista_de_adress.append(adress)

        while True:
            data = conn.recv(1024)

            if not data:
                print('Fechando conexao...')
                lista_de_conn.remove(conn)
                lista_de_adress.remove(adress)
                conn.close()
                break

            #Retornando a maensagem para todo cliente na rede
            for cada_conn in lista_de_conn:
                if cada_conn != conn:
                    cada_conn.sendall(data)

            print(f'Mensagem Recebida: {data.decode()}')

for _ in range(4):
    t = Thread(target=server_connection)
    t.start()

envioMensagem = Thread(target=enviar_mensagem)
envioMensagem.start()