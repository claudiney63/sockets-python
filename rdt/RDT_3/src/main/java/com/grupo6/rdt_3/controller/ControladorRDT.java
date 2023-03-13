package com.grupo6.rdt_3.controller;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JOptionPane;

public class ControladorRDT {

    private InetAddress host;
    private int port = 6000;
    private DatagramSocket skt;
    private int opc = 0;
    private String mensagem = "Esperando pacote...";

    private String ipEnvio = "192.168.1.9";
    private int portaEnvio = 4000;
    
    public ControladorRDT() {
        try {
            host = InetAddress.getLocalHost();
            skt = new DatagramSocket(port);

            Thread coreThread = new Thread(() -> {
                core();
            });
            coreThread.start();
        } catch (UnknownHostException | SocketException e) {
            JOptionPane.showMessageDialog(null, "Erro: " + e);
        }
    }
    
    private void delay(int delay) {
        try {
            Thread.sleep(delay);
        } catch (InterruptedException e) {
            JOptionPane.showMessageDialog(null, "Error: " + e);
        }
    }

    public void core() {
        byte[] buffer = new byte[1024];
        while (true) {
            try {
                DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
                skt.receive(packet); // receive data and client address
                
                String data = new String(packet.getData(), 0, packet.getLength());
                System.out.println(data);;

                String[] parts = data.split("||");

                if (data.equals("ack0") || data.equals("ack1")) {
                    InetAddress dest = InetAddress.getByName(ipEnvio);
                    switch (opc) {
                        case 0 -> {
                            mensagem = "Esperando comando...";
                        }
                        case 1 -> {
                            DatagramPacket sendPacket = new DatagramPacket(packet.getData(), packet.getLength(), dest, portaEnvio);
                            skt.send(sendPacket);
                            mensagem = "Transmitindo: \n" + data;
                        }
                        case 2 -> {
                            DatagramPacket sendPacket = new DatagramPacket(packet.getData(), packet.getLength(), dest, portaEnvio);
                            skt.send(sendPacket);
                            mensagem = "Reenviando: \n" + data;
                        }
                        case 3 -> {
                            mensagem = "Apagado: \n" + data;
                        }
                        case 4 -> {
                            delay(4000);
                            DatagramPacket sendPacket = new DatagramPacket(packet.getData(), packet.getLength(), dest, portaEnvio);
                            skt.send(sendPacket);
                            mensagem = "Ack com atraso";
                        }
                        case 5 -> {
                            String[] partss = data.split("|");
                            partss[2] = partss[2] + "0";
                            
                            data = "";
                            for (String string : partss) {
                                data += string;
                            }

                            System.out.println("Dado comificado: " + data);
                        
                            DatagramPacket sendPacket = new DatagramPacket(data.getBytes(), data.length(), dest, portaEnvio);
                            skt.send(sendPacket);
                            mensagem = "Checksum comrrompido";
                        }
                        default -> mensagem = "Opção inválida";
                    }
                } else {
                    //end dest, numSe, dado, ckesum, 
                    InetAddress dest = InetAddress.getByName("192.168.1.9");
                    int portDest = 7000;
                    // this.ipEnvio = parts[5];
                    // this.portaEnvio = Integer.valueOf(parts[6]);

                    switch (opc) {
                        case 0 -> {
                            mensagem = "Esperando comando...";
                        }
                        case 1 -> {
                            DatagramPacket sendPacket = new DatagramPacket(packet.getData(), packet.getLength(), dest, portDest);
                            skt.send(sendPacket);
                            mensagem = "Transmitindo: \n" + data;
                        }
                        case 2 -> {
                            DatagramPacket sendPacket = new DatagramPacket(packet.getData(), packet.getLength(), dest, portDest);
                            skt.send(sendPacket);
                            mensagem = "Retransmitindo";
                        }
                        case 3 -> {
                            mensagem = "Apagado: \n" + data;
                        }
                        case 4 -> {
                            DatagramPacket sendPacket = new DatagramPacket(packet.getData(), packet.getLength(), dest, portDest);
                            skt.send(sendPacket);
                            mensagem = "Ack com atraso";
                        }
                        case 5 -> {
                            String[] partss = data.split("|");
                            partss[2] = partss[2] + "0";
                            
                            data = "";
                            for (String string : partss) {
                                data += string;
                            }

                            System.out.println("Dado comificado: " + data);
                        
                            DatagramPacket sendPacket = new DatagramPacket(data.getBytes(), data.length(), dest, portaEnvio);
                            skt.send(sendPacket);
                            mensagem = "Checksum comrrompido";
                        }
                        default -> {
                        }
                    }
                }
            }catch (IOException ex) {
                Logger.getLogger(ControladorRDT.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }
    
    public String getHostAddress(){
        return host.getHostAddress();
    }
    
    public int getHostPort(){
        return port;
    }
    
    public void setOpc(int opc){
        this.opc = opc;
    }
    
    public String getMensagem(){
        return this.mensagem;
    }

}