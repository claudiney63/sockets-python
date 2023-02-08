from random import randint
import socket
import threading

HOST_SUPER = '192.168.0.37'
HOST = socket.gethostbyname(socket.gethostname())
PORT = randint(5001, 5999)

ID_NODE = 0

CONECTAR_COM = (HOST_SUPER, 5000)

class Node:
    def __init__(self, node_host = HOST, node_port = PORT, node_id = ID_NODE):
        self.node_host = node_host
        self.node_port = node_port
        self.node_id = node_id
        self.contact_list = {}
        self.name_contact = ""

        # Socket servidor
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.node_host, self.node_port))
        self.server_socket.listen()

        # Socket Client / E envia a mensagem de identificação
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST_SUPER, 5000))
        self.client_socket.send(f'ID;{self.node_id};{self.node_port}'.encode('utf-8'))

    # def print_node(self):
    #     print(f'IP: {self.node_id} PORT: {self.node_port}')

    # def iniciar_conect_superNO(self):
    #     super_no_ip = input("Entre com o ip do super no: ")
    #     conecta_com = (super_no_ip, 5000)

    def iniciar(self):
        while True:
            # Aceita conexão pelo lado do servidor
            con, adr = self.server_socket.accept()

            while True:
                # Recebe a mensagem do no anterior ou do super no
                controller = con.recv(1024)
                comandos = controller.decode('utf-8')

                # Fecha conexão e espera uma nova
                if not controller:
                    break

                for comand in comandos.split('|'):
                    if comand == "":
                        continue

                    destino, mensager_controler, info = comand.split(';')

                    if (destino == "ID"):
                        if self.node_id == 0:
                            self.node_id = info
                        else:
                            self.client_socket.send(f'{comand}|'.encode())

                    # Aqui ele verifica se o id e a mensagem são para esse no, 
                    # caso não seja para esse no ele repassa a info para frente
                    elif destino[0] == f'P':
                        if destino != f'P{self.node_id}':
                            self.client_socket.send(f'{comand}|'.encode('utf-8'))

                        elif destino == f'P{self.node_id}':
                            # Atualiza o cliente e sua conexão
                            if mensager_controler == 'CONNECT_WITH':
                                self.client_socket.close()

                                print()

                                CONECTAR_COM = (info[2:16], int(info[19:23]))
                                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                self.client_socket.connect(CONECTAR_COM)

                            # Recebe um novo identificador e manda para o proximo no, e atualiza
                            if mensager_controler == 'NEW_ID':
                                self.node_id = int(info)
                                info = self.node_id + 1
                                self.client_socket.send(f"P{int(destino[1])+1};{mensager_controler};{info}|".encode("utf-8"))

                            if mensager_controler == 'FINDED':
                                print(f'Contato encontrado: {info}')
                                self.contact_list[self.name_contact] = info

                        #Caso a mensagem recebida for de busca
                        elif destino == 'SC':
                            if info in self.contact_list:
                                self.client_socket.send(f"{mensager_controler};FINDED;{self.contact_list[info]}|".encode("utf-8"))
                            
                            else:
                                if mensager_controler == f'P{self.node_id}':
                                    print('Contato não encontrado!')
                                else:
                                    self.client_socket.send(f"{comand}|".encode("utf-8"))

                        #Caso a mensagem recebida for para o super no
                        elif destino == 'TK':
                            self.client_socket.send(f'{comand}Z'.encode('utf-8'))


if __name__ == '__main__':
    node1 = Node()

    threading.Thread(target=node1.iniciar).start()
