import socket
from threading import Thread

HOST = '192.168.0.37'
PORT = 5000

class SuperNO:
    def __init__(self, host, port):
        self.connect_to = None
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5000
        self.peers_list = [(socket.gethostbyname(socket.gethostname()), 5000)]
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind((host, port))
        self.servidor.listen()

    def start(self):
        for _ in range(3):
            Thread(target=self.run).start()

    def run(self):
        while True:
            con, adr = self.servidor.accept()

            while True:
                print(self.peers_list)

                data_received = con.recv(1024)
                comandos_recebidos = data_received.decode("utf-8")

                if not data_received:
                    break

                for comando in comandos_recebidos.split("|"):
                    if comando == "":
                        continue

                    print(f"\nCOMANDO DO SUPER NÓ: ")
                    destino, message_controller, info_add = comando.split("//")
                    print(f'Destino: {destino}')
                    print(f'Mensagem de Controler: {message_controller}')
                    print(f'Info Adicional: {info_add}\n')

                    self.entrada_node(destino, info_add, adr)

                    self.entrada_novo_node(destino, message_controller, comando)

                    self.controller_super_no(destino, message_controller, info_add)

                    self.busca_arquivo(destino, comando)

    def entrada_node(self, destino, info_add, adr):
        """
        Essa função entrada_node que controla a adição de novos nós em uma rede peer-to-peer. 
        Se a mensagem recebida tiver o destino "ID", o endereço do novo nó é adicionado à lista de pares peers_list.
        Se a lista tiver apenas um nó, o super nó se conecta a ele enviando uma mensagem com o comando "NOVO_ID" 
        e o número de identificação atual (0). Se já houver mais de um nó, o último nó na lista é notificado 
        para se conectar ao novo nó enviando uma mensagem com o comando "CONECTAR_NODE" e o endereço do novo nó. 
        Além disso, uma mensagem com o comando "NOVO_ID" é enviada para o novo nó informando-o sobre seu número de identificação.
        """
        if (destino == "ID"):
            self.peers_list.append((adr[0], int(info_add)))

            # Se for o primeiro peer da rede, tracker se conecta com ele
            if (len(self.peers_list) == 2):
                self.connect_to = self.peers_list[1]
                self.cliente.connect(self.connect_to)
                self.cliente.send(
                    f"ID//NOVO_ID//{len(self.peers_list) - 1}|".encode("utf-8"))

            # Se não for o unico par da rede, vai ser o novo ultimo par
            if (len(self.peers_list) > 2):
                ultimo_par = len(self.peers_list) - 2
                self.cliente.send(
                    f"P{ultimo_par}//CONECTAR_NODE//{self.peers_list[-1]}|".encode("utf-8"))
                self.cliente.send(
                    f"ID//NOVO_ID//{len(self.peers_list) - 1}|".encode("utf-8"))

    def entrada_novo_node(self, destino, message_controller, comando):
        """
        Esta função manipula a entrada de um novo nó em uma rede P2P. Se o destino da mensagem for um peer (identificado pelo prefixo "P"), 
        então a mensagem é processada. Se a mensagem contém o controle "NOVO_ID", a função não faz nada. Caso contrário, a mensagem é 
        repassada para o próximo peer na rede.
        """
        if (destino[0] == "P"):
            if message_controller == "NOVO_ID":
                pass
            else:
                self.cliente.send(f"{comando}|".encode("utf-8"))

    def controller_super_no(self, destino, message_controller, info_add):
        """
        A função tem três parâmetros de entrada: destino, message_controller, info_add. A lógica da função depende do valor de destino, que deve ser "SUPER_NO" 
        para a função ser executada. Se o valor de message_controller for "REMOVER_NODE", a função remove um nó da lista de peers self.peers_list, 
        dependendo do valor de info_add[1], que é o índice do nó a ser removido na lista. 
        
        Se o nó a ser removido for o último da lista, 
        ele é removido e uma mensagem é enviada para o penúltimo nó, solicitando que ele se conecte ao primeiro nó da lista. Se o nó a ser removido 
        não for o primeiro nem o último, ele é removido da lista e duas mensagens são enviadas, uma para o nó anterior, solicitando que se conecte ao 
        nó imediatamente após o removido, e outra para o próximo nó, informando que o seu ID agora é o mesmo do nó removido.

        Se o nó a ser removido for o primeiro, a função remove ele da lista, fecha a conexão atual e estabelece uma nova conexão com o 
        segundo nó da lista. Uma mensagem é enviada ao segundo nó, informando que ele é agora o nó de ID 1.
        """
        if (destino == "SUPER_NO"):
            if (message_controller == "REMOVER_NODE"):
                if int(info_add[1]) == len(self.peers_list) - 1:
                    self.peers_list.pop(-1)
                    self.cliente.send(
                        f"P{len(self.peers_list) - 1}//CONECTAR_NODE//{self.peers_list[0]}|".encode("utf-8"))

                elif info_add[1] != "1":
                    node_saida = int(info_add[1])
                    self.peers_list.pop(node_saida)

                    node_anterior = node_saida - 1

                    cliente.send(
                        f"P{node_anterior}//CONECTAR_NODE//{self.peers_list[node_saida]}|".encode("utf-8"))
                    cliente.send(
                        f"P{node_saida + 1}//NOVO_ID//{node_saida}|".encode("utf-8"))

                elif info_add[1] == "1":
                    self.peers_list.pop(1)
                    cliente.close()
                    connect_to = self.peers_list[1]

                    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    cliente.connect(connect_to)
                    print("Novo nó conectado")
                    cliente.send(f"P2//NOVO_ID//1|".encode("utf-8"))

    def busca_arquivo(self, destino, comando):
        """
        Esta função realiza uma busca de um arquivo em algum outro node na rede. A função "busca_arquivo" recebe 
        como parâmetros "destino" e "comando". Se o valor de "destino" for "BUSCA_ARQUIVO", o código envia a 
        mensagem de busca de arquivo (representada por "comando") para o socket conectado (representado por "self.cliente"). 
        A mensagem é enviada em formato de codificação "utf-8" com o caractere "|" no final.
        """
        if (destino == "BUSCA_ARQUIVO"):
            self.cliente.send(f"{comando}|".encode("utf-8"))

if __name__ == "__main__":
    supeNo = SuperNO(HOST, PORT)
    supeNo.start()
