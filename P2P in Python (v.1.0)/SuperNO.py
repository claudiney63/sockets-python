import socket
from threading import Thread

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
                commands = data_received.decode("utf-8")

                if not data_received:
                    break

                for command in commands.split("|"):
                    if command == "":
                        continue

                    print(f"\nCOMANDO DO SUPER NÓ: ")
                    destino, message_controller, info_add, = command.split(";")
                    print(f'Destino: {destino}')
                    print(f'Mensagem de Controler: {message_controller}')
                    print(f'Info Adicional: {info_add}\n')

                    self.entrada_node(destino, info_add, adr)

                    self.entrada_novo_node(destino, message_controller, command)

                    self.controller_super_no(destino, message_controller, info_add)

                    self.busca_contato(destino, command)

    def entrada_node(self, destino, info_add, adr):
        if (destino == "ID"):
            self.peers_list.append((adr[0], int(info_add)))

            # Se for o primeiro peer da rede, tracker se conecta com ele
            if (len(self.peers_list) == 2):
                self.connect_to = self.peers_list[1]
                self.cliente.connect(self.connect_to)
                self.cliente.send(
                    f"ID;NOVO_ID;{len(self.peers_list) - 1}|".encode("utf-8"))

            # Se não for o unico par da rede, vai ser o novo ultimo par
            if (len(self.peers_list) > 2):
                ultimo_par = len(self.peers_list) - 2
                self.cliente.send(
                    f"P{ultimo_par};CONECTAR_NODE;{self.peers_list[-1]}|".encode("utf-8"))
                self.cliente.send(
                    f"ID;NOVO_ID;{len(self.peers_list) - 1}|".encode("utf-8"))

    def entrada_novo_node(self, destino, message_controller, command):
        if (destino[0] == "P"):
            if message_controller == "NOVO_ID":
                pass
            else:
                self.cliente.send(f"{command}|".encode("utf-8"))

    def controller_super_no(self, destino, message_controller, info_add):
        if (destino == "SUPER_NO"):
            if (message_controller == "REMOVER_NODE"):
                if int(info_add[1]) == len(self.peers_list) - 1:
                    self.peers_list.pop(-1)
                    self.cliente.send(
                        f"P{len(self.peers_list) - 1};CONECTAR_NODE;{self.peers_list[0]}|".encode("utf-8"))

                elif info_add[1] != "1":
                    node_saida = int(info_add[1])
                    self.peers_list.pop(node_saida)

                    node_anterior = node_saida - 1

                    cliente.send(
                        f"P{node_anterior};CONECTAR_NODE;{self.peers_list[node_saida]}|".encode("utf-8"))
                    cliente.send(
                        f"P{node_saida + 1};NOVO_ID;{node_saida}|".encode("utf-8"))

                # Caso o no que saiu seja o primeiro
                elif info_add[1] == "1":
                    self.peers_list.pop(1)
                    cliente.close()
                    connect_to = self.peers_list[1]

                    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    cliente.connect(connect_to)
                    print("Conectado com o novo par")
                    cliente.send(f"P2;NOVO_ID;1|".encode("utf-8"))

    def busca_contato(self, destino, command):
        # Mensagem de busca de contato nas lista telefonicas
        if (destino == "BUSCAR_CONTATO"):
            self.cliente.send(f"{command}|".encode("utf-8"))

if __name__ == "__main__":
    supeNo = SuperNO('192.168.0.37', 5000)
    supeNo.start()
