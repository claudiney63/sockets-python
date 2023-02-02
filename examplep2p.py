import socket
import threading

class P2PNode:
    def __init__(self, host, port, next_node_host, next_node_port):
        self.next_node_host = next_node_host
        self.next_node_port = next_node_port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        
    def work_as_client(self):
        while True:
            # Connect to the next node in the P2P network
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.next_node_host, self.next_node_port))
            
            # Send a message to the next node
            message = input('Digite uma mensagem: ')
            client.send(message.encode())
            
            # Receive a message from the next node
            received = client.recv(1024).decode()
            print(received)
            
            # Close the connection
            client.close()
            
    def receive_message(self):
        while True:
            conn, addr = self.server.accept()
            received = conn.recv(1024).decode()
            print(received)
            
            # Send the received message to the next node
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.next_node_host, self.next_node_port))
            client.send(received.encode())
            client.close()

node1 = P2PNode(host='192.168.0.37', port=5000, next_node_host='192.168.0.37', next_node_port=5001)

client_thread1 = threading.Thread(target=node1.work_as_client)
client_thread1.start()
receive_thread1 = threading.Thread(target=node1.receive_message)
receive_thread1.start()