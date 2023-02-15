import socket
import os
from random import randint
from threading import Thread
from time import sleep

HOST = input('Digite o endereço do super no: ')

class Node:

    def __init__(self, node_ip):
        self.node_ip = node_ip
        self.node_port = randint(5001, 5999)
        self.super_ip = HOST
        self.super_port = 5000
        self.id = 0
        self.connect_to = (self.super_ip, self.super_port)
        self.nome_arqui = ''

        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind((self.node_ip, self.node_port))
        self.servidor.listen()

        try: 
            self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cliente.connect((self.super_ip, self.super_port))
            self.cliente.send(
                f"ID//{self.node_ip}//{self.node_port}".encode("utf-8"))
            
        except:
            print('\nNão foi possivel iniciar o socket cliente!')
            sleep(1)
            print('\nFechando aplicação...')
            sleep(2)
            os._exit(0) 


    def start_node(self):
        Thread(target=self.new_node).start()
        Thread(target=self.central_comandos).start()


    def new_node(self):
        while True:
            con, adr = self.servidor.accept()

            while True:

                data_received = con.recv(1024)
                comandos_recebidos = data_received.decode('utf-8')

                if not data_received:
                    break

                for comando in comandos_recebidos.split('|'):
                    if comando == "":
                        continue

                    destino, message_controller, info_add = comando.split("//")

                    self.verifica_id(destino, info_add, comando)

                    self.receber_mensagem(destino, comando, message_controller, info_add)

                    self.busca_arquivo(destino, message_controller, comando, info_add)

                    if destino == "SUPER_NO":
                        self.cliente.send(f"{comando}|".encode("utf-8"))


    def verifica_id(self, destino, info_add, comando):
        """
        A função verifica se o valor de "destino" é igual a "ID". Se for, ele verifica se o ID deste nó é igual a zero. 
        Se for, ele atribui o valor de "info_add" ao ID do nó. Se não for, ele envia uma mensagem codificada para o cliente do pro//imo nó
        com o comando especificado. A função verifica um identificador único de cada nó
        e se o nó já tem um ID ou se precisa receber um novo ID.
        """
        if (destino == "ID"):
            if self.id == 0:
                self.id = info_add
            else:
                self.cliente.send(f"{comando}|".encode("utf-8"))


    def receber_mensagem(self, destino, comando, message_controller, info_add):
        """
        Essa função verifica se a mensagem é destinada a um node específico (verificado pelo primeiro caractere da variável "destino" ser igual a "P"). 
        Se for para outro node, a mensagem é reencaminhada para o próximo. Se for para esse node, ele executa o comando especificado na mensagem.

        Os três comandos que ele pode receber são:
        "CONECTAR_NODE": o peer se conecta a outro node, com o endereço IP e porta especificados em "info_add"
        "NOVO_ID": o node atualiza seu ID para o valor especificado em "info_add" e envia uma mensagem para o próximo peer com o ID atualizado.
        "ENCONTROU_ARQUIVO": o node retorna o conteudo do arquivo encontrado.
        """
        if destino[0] == f'P':
            if destino != f"P{self.id}":
                self.cliente.send(f"{comando}|".encode("utf-8"))

            elif destino == f"P{self.id}":
                if message_controller == "CONECTAR_NODE":

                    id_conect = info_add.split(",")[0].split("'")[1]
                    port_conect = info_add.split(",")[1].split(')')[0].split(' ')[1]

                    self.cliente.close()

                    self.connect_to = (f'{id_conect}', int(port_conect))
                    self.cliente = socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM)
                    self.cliente.connect(self.connect_to)

                if message_controller == "NOVO_ID":
                    self.id = int(info_add)
                    info_add = self.id + 1
                    self.cliente.send(
                        f"P{int(destino[1])+1}//{message_controller}//{info_add}|".encode("utf-8"))

                if message_controller == "ENCONTROU_ARQUIVO":
                    print(f"\nArquivo encontrado!\n")
                    with open(self.nome_arqui, 'w') as file:
                        file.write(info_add)


    def busca_arquivo(self, destino, message_controller, comando, info_add):
        """
        A função busca um arquivo  
        Se o arquivo procurado estiver na rede, o node envia a informação de onde o arquivo foi encontrado para o destinatário da mensagem. 
        Caso contrário, se o destinatário da mensagem for o próprio node, ele imprime "Arquivo não encontrado". 
        Se o destinatário não for o próprio node, a mensagem é reencaminhada para outro node.
        """
        if destino == "BUSCA_ARQUIVO":
            pasta = './'
            for diretorio, subpastas, arquivos in os.walk(pasta): 
                for arquivo in arquivos:
                    if os.path.join(diretorio, arquivo) == './' + info_add: # verifica os arquivos do diretorio
                        conteudo_linhas = ""
                        with open(info_add, 'rb') as file:
                            for data in file.readlines():
                                conteudo_linhas += data.decode()

                        self.cliente.send(
                            f"{message_controller}//ENCONTROU_ARQUIVO//{conteudo_linhas}|".encode("utf-8"))
                        return

            # se não encontrou
            if message_controller == f"P{self.id}":
                print("Arquivo não encontrado")
            else:
                print("Repassando para outro node!")
                self.cliente.send(f"{comando}|".encode("utf-8"))


    def central_comandos(self):

        while True:

            try: 
                print("\n======= MENU =======")
                print("1 - Ler arquivo")
                print("2 - Buscar arquivo")
                print("3 - Listar arquivos")
                print("4 - ID Atual")
                print("5 - Pares atuais")
                print("6 - Sair da rede")
                print("\n====================")

                escolha = int(input("\nDigite sua escolha: "))

                if escolha == 1:
                    self.nome_arqui = input("Nome arquivo: ")
                    with open(self.nome_arqui, 'rb') as file:
                        for data in file.readlines():
                            print(data)

                if escolha == 2:
                    self.nome_arqui = input("Nome arquivo: ")
                    self.cliente.send(f"BUSCA_ARQUIVO//P{self.id}//{self.nome_arqui}".encode("utf-8"))

                if escolha == 3:
                    pasta = './'

                    print('\n======= Arquivos =======\n')
                    for diretorio, subpastas, arquivos in os.walk(pasta):
                        for arquivo in arquivos:
                            print(os.path.join(diretorio, arquivo))
                    print('\n')

                if escolha == 4:
                    print(f"Olá sou o P{self.id}")

                if escolha == 5:
                    print(self.connect_to)
                
                if escolha == 6:
                    self.cliente.send(f"SUPER_NO//REMOVER_NODE//P{self.id}".encode("utf-8"))
                    self.cliente.close()
                    self.servidor.close()
                    print(f"Node P{self.id} saiu da rede!!")
                    os._exit(0)

                if escolha <= 0 and escolha > 6:
                    print("\nInforme uma opção valida!")

            except:
                self.cliente.send(f"SUPER_NO//REMOVER_NODE//P{self.id}".encode("utf-8"))
                self.cliente.close()
                self.servidor.close()
                print("Ocorreu um erro inesperado!")
                os._exit(0)


if __name__ == "__main__":
    novo_node = Node('192.168.3.2')
    novo_node.start_node()
