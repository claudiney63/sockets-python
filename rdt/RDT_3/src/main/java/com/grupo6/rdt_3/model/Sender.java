package com.grupo6.rdt_3.model;

import java.io.IOException;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

import com.grupo6.rdt_3.util.FileOperation;

public class Sender {
    
    String ipControler;
    String ipLocal;
    String ipDestino;

    int portaControler = 5000;

    public Sender(String nomeArq) throws UnknownHostException{

        ipLocal = InetAddress.getLocalHost().getHostAddress(); // pegando ip da máquina local na rede

        //System.out.println("\nSeu ip: " + ipLocal + "\n");

        enviaArquivo(nomeArq);
    }

    private void enviaArquivo(String nomeArq){
    
        FileOperation fileOperation = new FileOperation();

        int numeroSequencia = 1;
        for (String linha : fileOperation.abreArquivo(nomeArq)) { /* envia linha por linha */
            String checksum = calculateChecksum(linha);
            String lineSeq = (linha + "//" + numeroSequencia + "//" + checksum);
            send(lineSeq, numeroSequencia, checksum);
            numeroSequencia++;
        }
    }

    private void send(String line, int seqNumb, String checksum) {
        try {
            byte[] lineData = line.getBytes();
            InetAddress interceptorAdress = InetAddress.getByName("localhost");
            boolean ackReceived = false;
            boolean currentSeqAck = false;
            
            while (!ackReceived) {
                try (DatagramSocket socketToInterceptor = new DatagramSocket()) {
                    
                    socketToInterceptor.setSoTimeout(300); // definindo um tempo limite de 5 segundos

                    System.out.println(line);

                    DatagramPacket packet = new DatagramPacket(lineData, lineData.length, interceptorAdress, portaControler);
                    socketToInterceptor.send(packet); //envio a linha atual dentro de um datagramaPacket

                    byte[] ackData = new byte[1024]; //crio um novo datagramaPacket para receber o ACK vindo do receiver
                    DatagramPacket ackPacket = new DatagramPacket(ackData, ackData.length);

                    try (
                        DatagramSocket socketFromInterceptor = new DatagramSocket(6000)) {
                        socketFromInterceptor.setSoTimeout(300);
                        while(!currentSeqAck){
                            socketFromInterceptor.receive(ackPacket);
        
                            String ackMessage = new String(ackPacket.getData(), 0, ackPacket.getLength()); 
                            System.out.println("ack = " + ackMessage);                   
                            String parts[] = ackMessage.split("/");
                            //Se o checksum conferir então eu dou ACK e continuo para a próxima linha do arquivo senão mando de novo a mesma linha
                            if ((Integer.parseInt(parts[1]) == seqNumb && !checksum.equals(parts[2])) || (!(Integer.parseInt(parts[1]) == seqNumb) && !checksum.equals(parts[2]))) {
                                break;
                            }else if(!(Integer.parseInt(parts[1]) == seqNumb) && checksum.equals(parts[2])){
                                continue;
                            }else if(Integer.parseInt(parts[1]) == seqNumb && checksum.equals(parts[2])){
                                ackReceived = true;
                                currentSeqAck = true;
                            }
                        }

                    }catch (SocketTimeoutException e) {
                        System.out.println("Timeout"); //Se o temporizador estourar, seja por prematuridade seja por descarte de pacote, o sender envia a lina de novo
                        continue;
                    }
                }
            }
        } catch (Exception e) {
            // TODO: handle exception
        }
    }
    
    /* Função que faz o calculo do checksum */
    private String calculateChecksum(String input) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hashInBytes = md.digest(input.getBytes(StandardCharsets.UTF_8));

            StringBuilder sb = new StringBuilder();
            for (byte b : hashInBytes) {
                sb.append(String.format("%02x", b));
            }
            return sb.toString();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            return null;
        }
    }
    
}