import socket

HOST = 'localhost'
PORT = 50000

#usando ipv4 e TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

s.listen() 

print('Aguardando conexao...')

conn, adress = s.accept()

print(f'Conectado em: {adress}')

while True:
    data = conn.recv(1024)
    if not data:
        print('Fechando conexao...')
        conn.close()
        break
    conn.sendall(data) #retornando a mensagem para o cliente