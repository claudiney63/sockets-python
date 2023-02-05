import socket
import threading

HOST = '192.168.0.37'
PORT = 5000

class P2P:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.nodes = []

    def iniciar(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind((self.host, self.port)) #Conectando ao servidor, host e porta
        servidor.listen()
        print(f'\nSuper nó escutando em Host: {self.host}, Porta: {self.port}...')

        while True:
            client, address = servidor.accept()
            client.send(f'\nOlá, bem-vindo a rede P2P {self.host}!!'.encode())
            self.nodes.append(client)
            mensagem = input("\nEnvie uma mensagem: ")
            if mensagem == 'Exit':
                client.close()
            client.sendall(mensagem.encode())
            threading.Thread(target=self.clientes_conectados, args=(client,)).start()
            

    def clientes_conectados(self, client):
        while True:
            mensagem = client.recv(1024)
            if not mensagem:
                print(f'Nó {client.getpeername()} desconectado!')
                self.nodes.remove(client)
                client.close()
                break
            else:
                print(f'Mensagem recebida de {client.getpeername()} : {mensagem.decode()}')
                for node in self.nodes:
                    if node != client:
                        node.sendall(mensagem)
    
    def conectando_em_No(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        self.nodes.append(client)
        while True:
            mensagem = input("\nEnvie uma mensagem: ")
            if mensagem == 'Exit':
                client.close()
            client.sendall(mensagem.encode())
            threading.Thread(target=self.clientes_conectados, args=(client,)).start()
            

if __name__ == "__main__":
    novo_node = P2P(HOST, PORT)
    novo_node.iniciar()
