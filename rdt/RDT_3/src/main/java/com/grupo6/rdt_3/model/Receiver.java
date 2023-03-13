package com.grupo6.rdt_3.model;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Receiver {
    
    String my_ip = "10.0.0.108";
    String core_ip = "10.0.0.108";
    int ack_number = 0;
    
    public void receber(){
        try {
            DatagramSocket skt =  new DatagramSocket(7000);
           
            Runnable receiveRunnable;
            receiveRunnable = new Runnable() {
                @Override
                public void run() {
                    while (true) {
                        try {
                            byte[] buf = new byte[1024];
                            DatagramPacket packet = new DatagramPacket(buf, buf.length);
                            skt.receive(packet);
                            
                            String data = new String(packet.getData(), 0, packet.getLength());
                            
                            String[] parts = data.split("\\|");
                            
                            String ip = parts[0];
                            String serial_number = parts[1];
                            
                            System.out.println("=================================");
                            System.out.println("Ip remetente: " + ip);
                            System.out.println("Serial Number: " + serial_number.charAt(0));
                            System.out.println("Mensagem recebida: " + serial_number.substring(1));
                            System.out.println("=================================\n");
                            
                            if (Integer.parseInt(String.valueOf(serial_number.charAt(0))) == ack_number) {
                                byte[] ackData = ("ack" + ack_number).getBytes();
                                
                                DatagramPacket ackPacket = new DatagramPacket(ackData, ackData.length, InetAddress.getByName(core_ip), 6000);
                                skt.send(ackPacket);
                                
                                if (ack_number == 0) {
                                    ack_number = 1;
                                } else {
                                    ack_number = 0;
                                }
                            } else {
                                byte[] ackData = ("ack" + Integer.valueOf(String.valueOf(serial_number.charAt(0)))).getBytes();
                                DatagramPacket ackPacket = new DatagramPacket(ackData, ackData.length, InetAddress.getByName(core_ip), 6000);
                                skt.send(ackPacket);
                                
                                System.out.println("Received wrong ack. Pkg deleted");
                            }
                        } catch (IOException ex) {
                            Logger.getLogger(Receiver.class.getName()).log(Level.SEVERE, null, ex);
                        }
                    }
                }
            };
            new Thread(receiveRunnable).start();
        } catch (SocketException ex) {
            Logger.getLogger(Receiver.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

}