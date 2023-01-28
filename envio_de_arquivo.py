import socket

# Cria um socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço IP e a porta do par a se conectar
peer_ip = '192.168.0.37'
peer_port = 50000

# Tenta se conectar ao par
s.connect((peer_ip, peer_port))

# Envia o arquivo PDF para o par conectado
with open('arquivo.pdf', 'rb') as f:
    data = f.read()
    s.sendall(data)
    print('Enviando arquivo PDF...')
print('Arquivo enviado com sucesso')

# Fecha a conexão com o par
s.close()