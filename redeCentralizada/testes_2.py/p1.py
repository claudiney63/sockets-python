import socket
import threading

class Node_P2P:
    def __init__(self, idPeer, host, port, nextNode):
        self.idPeer = idPeer
        self.host = host
        self.port = port
        self.nextNode = nextNode
        self.status = {
            'id': idPeer,
            'id_sucessor': ''
        }
        self.nodes = []

    def iniciar_super_no(self):
        super_no = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        super_no.bind((self.host, self.port))
        super_no.listen()
        print(f'\nSuper nó escutando em Host: {self.host}, Porta: {self.port}...')
        cont = 0

        while True:

            client, adress = super_no.accept()

            if cont == 0:
                threading.Thread(target=self.conectando_node, args=(self.host, self.nextNode)).start()
                cont = 1

            client.send(f'Olá {adress} bem-vindo a rede P2P!'.encode())
            self.nodes.append(client)
            
            threading.Thread(target=self.nodes_conectados, args=(client,)).start()

    def nodes_conectados(self, client):
        while True:

            mensagem = client.recv(1024)

            if not mensagem:
                print(f'\nNó {client.getpeername()} desconectado!')
                self.nodes.remove(client)
                client.close()
                break
            else:
                client.send(mensagem)
                print(f'\nMensagem recebida de {client.getpeername()} : {mensagem.decode()}')

    def conectando_node(self, host, port):

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        self.nodes.append(client)

        while True:
            mensagem = input('\nEnvie uma mnesagem: ')

            if mensagem == '' or mensagem == 'exit':
                client.close()
                break

            client.sendall(mensagem.encode())
            threading.Thread(target=self.nodes_conectados, args=(client,)).start()


if __name__ == '__main__':
    superNo = Node_P2P(1, '192.168.0.37', 5000, 5001).iniciar_super_no()