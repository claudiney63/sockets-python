

from tkinter import *
from tkinter import ttk

def gui_core():
    janela = Tk()
    janela.title("Menu de Interações")
    texto_port = Label(janela, text=string_ip_port)
    texto = Label(janela, text="Escolha uma da opções abaixo, o que deseja fazer com a mensagem?")
    texto.grid(column=0, row=1, padx=10, pady=10)
    texto_port.grid(column=0, row=0, padx=10, pady=10)

    botao1 = Button(janela, text="Reenviar normalmente", command=menu(1))
    botao1.grid(column=0, row=2, padx=10, pady=10)

    botao2 = Button(janela, text="Descartar pacote", command=menu(2))
    botao2.grid(column=0, row=3, padx=10, pady=10)

    botao3 = Button(janela, text="Enviar duplicado", command=menu(3))
    botao3.grid(column=0, row=4, padx=10, pady=10)

    botao4 = Button(janela, text="Apagar ack", command=menu(4))
    botao4.grid(column=0, row=5, padx=10, pady=10)

    texto_resposta = Label(janela, text="")
    texto_resposta.grid(column=0, row=6, padx=10, pady=10)

    janela.mainloop()
