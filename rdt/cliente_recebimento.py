from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname
from time import sleep
from threading import Thread, Lock

import zlib

my_ip = "192.168.1.9" # todo change to get a input or gambiarra
core_ip = "192.168.1.9"

skt = socket(AF_INET, SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP
skt.bind((my_ip, 7000)) # todo change to 7000 port

ack_number = 0

def receive():
    global skt, ack_number

    while True:
        data, addr = skt.recvfrom(1024) # receive data and client 
        data_check = data
        data = data.decode("utf-8")
        
        #print(data) #* debug

        ip, serial_number, checksum_enviado = data.split("|")

        print("=================================")
        print(f"Ip remetente: {ip}")
        print(f"Serial Number: {serial_number[0]}")
        print(f"Mensagem recebida: {serial_number[1:-1]}{serial_number[-1]}")
        checksum = checksum_calculator(f"{serial_number[1:-1]}{serial_number[-1]}")
        print(f"\nChecksum (enviado): {bin(int(str(hex(checksum_enviado)), 16))}")
        print(f"\nChecksum (recebido): {bin(int(str(hex(checksum)), 16))}")
        print("=================================\n")

        if bin(int(str(hex(checksum_enviado)), 16)) == bin(int(str(hex(checksum)), 16)):

            if int(serial_number[0]) == ack_number:
                skt.sendto(f"ack{ack_number}".encode("utf-8"), (core_ip, 6000))

                if ack_number == 0:
                    ack_number = 1
                else:
                    ack_number = 0
            else:
                skt.sendto(f"ack{int(serial_number[0])}".encode("utf-8"), (core_ip, 6000))
                print("Received wrong ack. Pkg deleted")
        else:
            if ack_number == 0:
                ack = 1
            else:
                ack = 0
            skt.sendto(f"ack{ack}".encode("utf-8"), (core_ip, 6000))
            print("Received wrong ack. Pkg deleted")

def checksum_calculator(data):
    checksum = zlib.crc32(data)
    return checksum

Thread(target=receive).start()