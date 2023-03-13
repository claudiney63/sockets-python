from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname, timeout
from time import sleep
from threading import Thread, Lock
import zlib

class Sender:
    def __init__(self, core_ip, sender_ip, receive_ip):
        self.core_ip = core_ip
        self.sender_ip = sender_ip
        self.receive_ip = receive_ip
        self.numero_de_serie = 0

        critical = Lock()
        self.critical = critical

        with self.critical:
            self.ack = False

        self.skt = socket(AF_INET, SOCK_DGRAM)  # AF_INET = IPV4 | SOCK_DGRAM = UDP
        self.skt.bind((self.sender_ip, 4000))

    def send(self):

        while True:
            data = input("\nEnvie uma mensagem: ")
            self.criar_segmento(self.receive_ip, self.skt, data)

    def criar_segmento(self, adrr: str,  skt: socket, data: str) -> None:

        checksum = self.checksum_calculator(data.encode())

        for i in range(0, len(data), 1024):
            segment_data = data[i:i+1024]
            segment = f"{adrr}|{self.numero_de_serie}{segment_data}|{checksum}"

            self.skt.sendto(segment.encode("utf-8"), (self.core_ip, 6000))

            while True:
                sleep(1)

                with self.critical:
                    if self.ack:
                        self.ack = False

                        break
                    else:
                        # todo change to 5000 port
                        self.skt.sendto(segment.encode("utf-8"), (self.core_ip, 6000))

            skt.settimeout(3)

            if self.numero_de_serie == 0:
                self.numero_de_serie = 1
            else:
                self.numero_de_serie = 0

    def receive(self):

        while True:
            try:
                # receive data and client address
                data, addr = self.skt.recvfrom(1024)
                data = data.decode("utf-8")

                if data == "ack0" and self.numero_de_serie == 0:
                    with self.critical:
                        print(f"Recebido ack {self.numero_de_serie}")
                        self.ack = True

                elif data == "ack1" and self.numero_de_serie == 1:
                    with self.critical:
                        print(f"Recebido ack {self.numero_de_serie}")
                        self.ack = True
            except timeout:
                print("except")

    def checksum_calculator(self, data):
        checksum = zlib.crc32(data)
        return checksum
    
    def run(self):
        Thread(target=self.receive).start()
        Thread(target=self.send).start()

if __name__ == "__main__":
    send = Sender("192.168.1.9", "192.168.1.9", "192.168.1.9")
    send.run()
