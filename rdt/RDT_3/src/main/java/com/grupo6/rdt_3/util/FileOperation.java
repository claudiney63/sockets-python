package com.grupo6.rdt_3.util;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

public class FileOperation {

    public FileOperation() {
    }

    public List<String> abreArquivo(String nomeArq){
        List<String> linhas = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(nomeArq))) {
            String line;
            while ((line = reader.readLine()) != null) {
               linhas.add(line);
            }
            reader.close();
        } catch (IOException e) {
            Logger.getLogger(FileOperation.class.getName()).log(Level.SEVERE, null, e);
        }
        return linhas;
    }
    
    public void escreveArquivo(String nomeArq){
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(nomeArq))) {
            String frases = "";
            for (int i = 1; i < 50; i++) {
                frases += "Linha " + i + "\n";
            }
            writer.write(frases);
        } catch (IOException e) {
            Logger.getLogger(FileOperation.class.getName()).log(Level.SEVERE, null, e);
        }
    }
    
}