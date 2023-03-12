from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname, timeout
from time import sleep
from threading import Thread, Lock
import zlib

core_ip = "192.168.1.9" # todo change to input("Enter ip of network: ")
my_ip = gethostbyname(gethostname()) # todo change to get a input or gambiarra
destino_ip = input("Enter ip of addressee: ")

serial_number = 0

critical = Lock()
with critical:
    ack = False

skt = socket(AF_INET, SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP
skt.bind((my_ip, 4000))

def send():
    global skt
    
    while True:
        data = input("\nEnter data to send: ")
        make_segments(destino_ip, skt, data)

def make_segments(addressee_addr: str,  skt: socket, data: str) -> None:
    global serial_number, ack

    checksum = checksum_calculator(data)

    for i in range(0, len(data), 1024):
        segment_data = data[i:i+1024]
        segment = f"{addressee_addr}|{serial_number}{segment_data}|{checksum}"

        skt.sendto(segment.encode("utf-8"), (core_ip, 6000))
        
        while True:
            sleep(1)

            with critical:
                if ack:
                    # print("Received ack")
                    ack = False
                    
                    break
                else:
                    skt.sendto(segment.encode("utf-8"), (core_ip, 6000)) # todo change to 5000 port
                    
        skt.settimeout(3)

        if serial_number == 0:
            serial_number = 1
        else:
            serial_number = 0

def receive():
    global skt, ack

    while True:
        try:
            data, addr = skt.recvfrom(1024) # receive data and client address
            data = data.decode("utf-8")
            if data == "ack0" and serial_number == 0:
                with critical:
                    print(f"Received right ack {serial_number}")
                    ack = True
            elif data == "ack1" and serial_number == 1:
                with critical:
                    print(f"Received rick ack {serial_number}")
                    ack = True
        except timeout:
            print("except")

        

def checksum_calculator(data):
    checksum = zlib.crc32(data)
    return checksum
        

Thread(target=receive).start()
Thread(target=send).start()