import socket
from threading import Thread

class Tracker:
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
        for _ in range(5):
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
                    
                    if(destino == "ID"):
                        self.peers_list.append((adr[0], int(info_add)))

                        # Se for o primeiro peer da rede, tracker se conecta com ele
                        if(len(self.peers_list) == 2):
                            self.connect_to = self.peers_list[1]
                            self.cliente.connect(self.connect_to)
                            self.cliente.send(f"ID;NOVO_ID;{len(self.peers_list) - 1}|".encode("utf-8"))

                        # Se não for o unico par da rede, vai ser o novo ultimo par
                        if(len(self.peers_list) > 2):
                            old_final_peer_number = len(self.peers_list) - 2
                            self.cliente.send(f"P{old_final_peer_number};CONECTAR_NODE;{self.peers_list[-1]}|".encode("utf-8"))
                            self.cliente.send(f"ID;NOVO_ID;{len(self.peers_list) - 1}|".encode("utf-8"))
                    elif(destino[0] == "P"):
                        if message_controller == "NOVO_ID":
                            pass
                        else:
                            self.cliente.send(f"{command}|".encode("utf-8"))
                    elif(destino == "SUPER_NO"):
                        if(message_controller == "REMOVER_NODE"):
                            if int(info_add[1]) == len(self.peers_list) - 1:
                                self.peers_list.pop(-1)
                                self.cliente.send(f"P{len(self.peers_list) - 1};CONECTAR_NODE;{self.peers_list[0]}|".encode("utf-8"))

                            elif info_add[1] != "1":
                                quit_number = int(info_add[1])
                                self.peers_list.pop(quit_number)
                                
                                before_number = quit_number - 1

                                cliente.send(f"P{before_number};CONECTAR_NODE;{self.peers_list[quit_number]}|".encode("utf-8"))
                                cliente.send(f"P{quit_number + 1};NOVO_ID;{quit_number}|".encode("utf-8"))

                            # Caso o no que saiu seja o primeiro
                            elif info_add[1] == "1":
                                self.peers_list.pop(1)
                                cliente.close()
                                connect_to = self.peers_list[1]

                                cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                cliente.connect(connect_to)
                                print("Conectado com o novo par")
                                cliente.send(f"P2;NOVO_ID;1|".encode("utf-8"))
                    
                    # Mensagem de busca de contato nas lista telefonicas
                    elif(destino == "BUSCAR_CONTATO"):
                        cliente.send(f"{command}|".encode("utf-8"))

if __name__ == "__main__":
    supeNo = Tracker('192.168.0.37', 5000)
    supeNo.start()
