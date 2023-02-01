import socket
import json
import threading

peer_ip = '192.168.0.37'
peer_port = 50000

class P2PNode:
    def __init__(self, host='192.168.0.37', port=5000):
        self.peers = []
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        
    def listen_for_peers(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            self.peers.append(conn)
            print(f'Connected to {str(addr)}')
            threading.Thread(target=self.work_as_client, args=(conn,)).start()
            
    def work_as_client(self, conn):
        while True:
            # Connect to another peer in the P2P network
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((peer_ip, peer_port))
            
            # Send a message to the other peer
            message = {'message': 'Hello, this is a message from the node.'}
            client.send(json.dumps(message).encode())
            
            # Receive a message from the other peer
            received = json.loads(client.recv(1024).decode())
            print(received)
            
            # Close the connection
            client.close()
    def broadcast_message(self, message):
        for peer in self.peers:
            peer.send(json.dumps(message).encode())
            
    def receive_message(self):
        while True:
            for peer in self.peers:
                try:
                    received = json.loads(peer.recv(1024).decode())
                    print(received)
                except:
                    pass

node = P2PNode()
listen_thread = threading.Thread(target=node.listen_for_peers)
listen_thread.start()
receive_thread = threading.Thread(target=node.receive_message)
receive_thread.start()