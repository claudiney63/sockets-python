import socket
from threading import Thread
from time import sleep

import zlib

host = "192.168.1.9"
port = 6000 # todo change to 5000 port

destino_ip = "192.168.1.9"
remetente_ip = "192.168.1.5"

skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP
skt.bind((host, port))

print(f"Host: {host} | Port: {port}")

opc = 1

def menu():
    global opc

    while True:
        print("\nMenu de Interações:")
        print("1 - Reenviar normalmente")
        print("2 - Descartar pacote")
        print("3 - Apagar ack")
        print("4 - Enviar ack com atraso")
        print("5 - Verificar Checksum")

        opc = int(input("O que deseja fazer com o pacote: "))
    
def core():
    global skt
    global opc

    while True:
        data, addr = skt.recvfrom(1024) # receive data and client address

        if data.decode("utf-8") == "ack0" or data.decode("utf-8") == "ack1":
            if opc == 1:
                skt.sendto(data, (remetente_ip, 4000))
            elif opc == 2:
                skt.sendto(data, (remetente_ip, 4000))
            elif opc == 3:
                pass
            elif opc == 4:
                sleep(2)
                skt.sendto(data, (remetente_ip, 4000))
            elif opc == 5:
                checksum = checksum_calculator(data)
                print(f"\nChecksum (hex): {bin(int(str(hex(checksum)), 16))}")
            else:
                print("Opção inválida")
        else:
            if opc == 1:
                skt.sendto(data, (destino_ip, 7000))
            elif opc == 2:
                pass
            elif opc == 3:
                skt.sendto(data, (destino_ip, 7000))
            elif opc == 4:
                skt.sendto(data, (destino_ip, 7000))
            elif opc == 5:
                checksum = checksum_calculator(data)
                print(f"\nChecksum (hex): {bin(int(str(hex(checksum)), 16))}")
            else:
                print("Opção inválida")

        # opc = 0

        print(f"\nReceived data: {data.decode()}")

def checksum_calculator(data):
    checksum = zlib.crc32(data)
    return checksum


Thread(target=menu).start()
Thread(target=core).start()