from random import randint
import socket
from threading import Thread

class Node:
    def __init__(self, node_ip):
        self.node_ip = node_ip
        self.node_port = randint(5001, 5999)
        self.super_ip = '192.168.232.204'
        self.super_port = 5000
        self.id = 0
        self.lista_contatos = {}
        self.nome_contact = ""
        self.number_contato = 0
        self.connect_to = (self.super_ip, self.super_port)

        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind((self.node_ip, self.node_port))
        self.servidor.listen()

        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect((self.super_ip, self.super_port))
        self.cliente.send(
            f"IDx{self.node_ip}x{self.node_port}".encode("utf-8"))

    def start_node(self):
        Thread(target=self.new_node).start()
        Thread(target=self.central_comandos).start()

    def new_node(self):
        while True:
            con, adr = self.servidor.accept()

            while True:

                data_received = con.recv(1024)
                commands = data_received.decode('utf-8')

                if not data_received:
                    break

                for command in commands.split('|'):
                    if command == "":
                        continue

                    destino, message_controller, info_add = command.split("x")

                    self.verifica_id(destino, info_add, command)

                    self.receber_mensagem(destino, command, message_controller, info_add)

                    self.buscar_contato(destino, message_controller, command, info_add)

                    if destino == "SUPER_NO":
                        self.cliente.send(f"{command}Z".encode("utf-8"))

    def verifica_id(self, destino, info_add, command):
        """
        A função verifica se o valor de "destino" é igual a "ID". Se for, ele verifica se o ID deste nó é igual a zero. 
        Se for, ele atribui o valor de "info_add" ao ID do nó. Se não for, ele envia uma mensagem codificada para o cliente do proximo nó
        com o comando especificado. A função verifica um identificador único de cada nó
        e se o nó já tem um ID ou se precisa receber um novo ID.
        """
        if (destino == "ID"):
            if self.id == 0:
                self.id = info_add
            else:
                self.cliente.send(f"{command}|".encode("utf-8"))

    def receber_mensagem(self, destino, command, message_controller, info_add):
        """
        Essa função verifica se a mensagem é destinada a um node específico (verificado pelo primeiro caractere da variável "destino" ser igual a "P"). 
        Se for para outro node, a mensagem é reencaminhada para o próximo. Se for para esse node, ele executa o comando especificado na mensagem.

        Os três comandos que ele pode receber são:
        "CONECTAR_NODE": o peer se conecta a outro node, com o endereço IP e porta especificados em "info_add"
        "NOVO_ID": o node atualiza seu ID para o valor especificado em "info_add" e envia uma mensagem para o próximo peer com o ID atualizado.
        "ENCONTROU_CONTATO": o node adiciona o contato com o nome especificado em "self.nome_contact" e endereço IP "info_add" na sua lista de contatos.
        """
        if destino[0] == f'P':
            if destino != f"P{self.id}":
                self.cliente.send(f"{command}|".encode("utf-8"))

            elif destino == f"P{self.id}":
                if message_controller == "CONECTAR_NODE":
                    # print(info_add.split(","))

                    id_conect = info_add.split(",")[0].split("'")[1]
                    port_conect = info_add.split(",")[1].split(')')[0].split(' ')[1]

                    # print(id_conect)
                    # print(port_conect)

                    self.cliente.close()

                    self.connect_to = (f'{id_conect}', int(port_conect))
                    self.cliente = socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM)
                    self.cliente.connect(self.connect_to)

                if message_controller == "NOVO_ID":
                    self.id = int(info_add)
                    info_add = self.id + 1
                    self.cliente.send(
                        f"P{int(destino[1])+1}x{message_controller}x{info_add}|".encode("utf-8"))

                if message_controller == "ENCONTROU_CONTATO":
                    print(f"\nContato encontrado: {info_add}")
                    self.lista_contatos[self.nome_contact] = info_add

    def buscar_contato(self, destino, message_controller, command, info_add):
        """
        A função busca um contato em uma lista de contatos mantida pelo objeto de um peer. 
        Se o contato procurado estiver na lista, o peer envia a informação de onde o contato foi encontrado para o destinatário da mensagem. 
        Caso contrário, se o destinatário da mensagem for o próprio peer, ele imprime "Contato não encontrado". 
        Se o destinatário não for o próprio peer, a mensagem é reencaminhada para outro peer.
        """
        if destino == "BUSCAR_CONTATO":
            if info_add in self.lista_contatos:
                self.cliente.send(
                    f"{message_controller}xENCONTROU_CONTATOx{self.lista_contatos[info_add]}|".encode("utf-8"))
            else:
                if message_controller == f"P{self.id}":
                    print("Contato não encontrado")
                else:
                    self.cliente.send(f"{command}|".encode("utf-8"))

    def central_comandos(self):
        while True:
            print("\nLISTA TELEFONICA")
            print("1 - Adicionar contato")
            print("2 - Listar contatos")
            print("3 - Buscar contato")
            print("4 - Meu ID")
            print("5 - Meus pares")
            print("6 - Sair da rede")

            escolha = int(input("\nDigite o que deseja: "))

            if escolha == 1:
                self.nome_contact = input("Nome: ")
                self.number_contato = int(input("Numero: "))

                self.lista_contatos[self.nome_contact] = self.number_contato
                print("Contato salvo!!")

            if escolha == 2:
                print(self.lista_contatos)

            if escolha == 3:
                self.nome_contact = input("Nome: ")

                if self.nome_contact in self.lista_contatos:
                    print(self.lista_contatos[self.nome_contact])
                else:
                    self.cliente.send(f"BUSCAR_CONTATOxP{self.id}x{self.nome_contact}".encode("utf-8"))

            if escolha == 4:
                print(f"Olá sou o P{self.id}")

            if escolha == 5:
                print(self.connect_to)

            if escolha == 6:
                self.cliente.send(f"SUPER_NOxREMOVER_NODExP{self.id}".encode("utf-8"))
                self.cliente.close()
                self.servidor.close()
                print(f"Node P{self.id} saiu da rede!!")


if __name__ == "__main__":
    novo_node = Node('192.168.232.204')
    novo_node.start_node()
