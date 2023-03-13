package com.grupo6.rdt_3;

import com.grupo6.rdt_3.view.Tela;

public class RDT_3  {

    public static void main(String[] args) {
        Tela tela = new Tela();
        tela.setVisible(true);
        
        Thread t = new Thread(tela);
        t.start();
    }
 
}
