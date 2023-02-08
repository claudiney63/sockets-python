import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('localhost', 7777))
print('conectado')

namefile = str(input('Arquivo>'))

client.send(namefile.encode())


with open('recebido.txt', 'wb') as file:
    while 1:
        data = client.recv(1000000)
        if not data:
            break
        file.write(data)

print(f'{namefile} recebido!\n')