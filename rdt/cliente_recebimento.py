from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname
from time import sleep
from threading import Thread, Lock
import zlib

class Receive:
    def __init__(self, core_ip, receive_ip):
        self.core_ip = core_ip
        self.receive_ip = receive_ip

        self.skt = socket(AF_INET, SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP
        self.skt.bind((self.receive_ip, 7000))

        self.ack_number = 0

    def receive(self):

        while True:
            data, addr = self.skt.recvfrom(1024) # receive data and client 
            data = data.decode("utf-8")

            ip, serial_number, checksum_enviado = data.split("|")

            print("=================================")
            print(f"Ip remetente: {ip}")
            print(f"Serial Number: {serial_number[0]}")
            print(f"Mensagem recebida: {serial_number[1:-1]}{serial_number[-1]}")

            msg = f"{serial_number[1:-1]}{serial_number[-1]}"
            checksum = self.checksum_calculator(msg.encode())

            print(f"Checksum (enviado): {bin(int(str(hex(checksum)), 16))}")

            print(f"Checksum (recebido): {bin(int(str(hex(checksum)), 16))}")
            print("=================================\n")

            if(self.compare_checksums(bin(int(str(hex(checksum)), 16)), bin(int(str(hex(checksum)), 16)))) == False:
                print("Checksum São iguais")

                if int(serial_number[0]) == self.ack_number:
                    self.skt.sendto(f"ack{self.ack_number}".encode("utf-8"), (self.core_ip, 6000))

                    if self.ack_number == 0:
                        self.ack_number = 1
                    else:
                        self.ack_number = 0
                else:
                    self.skt.sendto(f"ack{int(serial_number[0])}".encode("utf-8"), (self.core_ip, 6000))
                    print("Ack com erro. Pacote deletado")
            else:
                print("Checksum Não iguais")
                if self.ack_number == 0:
                    ack = 1
                else:
                    ack = 0
                self.skt.sendto(f"ack{ack}".encode("utf-8"), (self.core_ip, 6000))
                print("Ack com erro. Pacote deletado")

    def checksum_calculator(self, data):
        checksum = zlib.crc32(data)
        return checksum
    
    def compare_checksums(self, checksum1, checksum2):
        if len(checksum1) != len(checksum2):
            return False  # Checksums devem ter o mesmo tamanho

        for i in range(len(checksum1)):
            if checksum1[i] != checksum2[i]:
                return False  # Se houver diferença em qualquer bit, os checksums não são iguais

        return True  # Se chegarmos até aqui, os checksums são iguais
    
    def run(self):
        Thread(target=self.receive).start()

if __name__ == "__main__":
    receive = Receive("192.168.1.9", "192.168.1.9")
    receive.run()
