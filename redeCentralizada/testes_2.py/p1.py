import socket
import threading

class Node_P2P:
    def __init__(self, idPeer, host, port, nextNode):
        self.idPeer = idPeer
        self.host = host
        self.port = port
        self.nextNode = nextNode
        self.nodes = [(socket.gethostbyname(socket.gethostname()), 5000)]

    def iniciar_super_no(self):
        super_no = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        super_no.bind((self.host, self.port))
        super_no.listen(5)
                
        print(f'\nSuper nó escutando em Host: {self.host}, Porta: {self.port}...')

        while True:

            client, adress = super_no.accept()

            self.nodes.append(adress)

            if client:
                threading.Thread(target=self.conectando_node, args=(self.host, self.nextNode)).start()

            print(self.nodes)

            client.send(f'Olá {adress} bem-vindo a rede P2P!'.encode())
            
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
                new_mensage = f'{mensagem.decode()}'
                new_mensage = new_mensage.split(';')
                mensagem = new_mensage[-1]

                if new_mensage[0] == f'{self.idPeer}':
                    print(f'\nMensagem recebida de {client.getpeername()} : {mensagem}')
                elif new_mensage[0] > f'{len(self.nodes)}':
                    break
                else:
                    id_new = int(new_mensage[0], base = 10) + 1
                    new_mensage = f'{id_new};{mensagem}'
                    client.send(new_mensage.encode())

    def conectando_node(self, host, port):

        while True:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((host, port))

            while True:
                mensagem = input('\nEnvie uma mensagem: ')

                if mensagem == '' or mensagem == 'exit':
                    client.close()
                    break

                id = self.idPeer + 1

                mensagem = f'{id};{mensagem}'

                client.sendall(mensagem.encode())
                threading.Thread(target=self.nodes_conectados, args=(client,)).start()

if __name__ == '__main__':
    superNo = Node_P2P(1, '192.168.0.37', 5000, 5001).iniciar_super_no()