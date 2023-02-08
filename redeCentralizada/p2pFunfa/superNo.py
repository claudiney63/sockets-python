import socket

HOST = '192.168.0.37'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class SuperNode:
    def __init__(self, node_id, port, next_node_ip, next_node_port):
        self.node_id = node_id
        self.port = port
        self.next_node_ip = next_node_ip
        self.next_node_port = next_node_port

        server_socket.bind((HOST, 5000))
        server_socket.listen()
        
    def start(self):
        print(f"No {self.node_id} iniciado na porta {self.port}")
        
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"No {self.node_id} esperando mensagem de {client_address}")
            message = client_socket.recv(1024).decode('utf-8')
            self.send(message)
            
    def send(self, message):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.node_id, 5000))
        client_socket.send(message.encode('utf-8'))
        
if __name__ == '__main__':
    node1 = SuperNode(0, 5000, HOST, 5001)
    
    node1.start()
