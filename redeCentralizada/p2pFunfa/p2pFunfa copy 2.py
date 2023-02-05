import socket

HOST = '192.168.0.37'

class Node:
    def __init__(self, node_id, port, next_node_ip, next_node_port):
        self.node_id = node_id
        self.port = port
        self.next_node_ip = next_node_ip
        self.next_node_port = next_node_port
        
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, self.port))
        server_socket.listen()
        
        print(f"Node {self.node_id} started on port {self.port}")
        
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Node {self.node_id} received message from {client_address}")
            message = client_socket.recv(1024).decode('utf-8')
            print(f"Node {self.node_id} forwarding message to node {self.next_node_ip}:{self.next_node_port}")
            self.send(message)
            
    def send(self, message):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.next_node_ip, self.next_node_port))
        client_socket.send(message.encode('utf-8'))
        
if __name__ == '__main__':
    node1 = Node(3, 5002, HOST, 5000)
    # node2 = Node(2, 5001, '127.0.0.1', 5002)
    # node3 = Node(3, 5002, '127.0.0.1', 5003)
    # node4 = Node(4, 5003, '127.0.0.1', 5004)
    # node5 = Node(5, 5004, '127.0.0.1', 5000)
    
    node1.start()
    # node2.start()
    # node3.start()
    # node4.start()
    # node5.start()
