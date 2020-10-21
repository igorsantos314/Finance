from tkinter import *
from datetime import date
import calendar
from tkinter import ttk
from tkinter import messagebox

from FinanceDataBase import *

class financeInterface(Frame):

    def __init__(self):
        #OBJETO DE BANCO DE DADOS
        self.bancoDados = bd()

        #DEFAULT
        self.verdeClaro = 'MediumSpringGreen'
        self.fontStyleUpper = 'Monaco 30 bold'
        self.tomato = 'Tomato'
        self.gold= 'PaleGoldenrod'
        self.azulClaro = 'PowderBlue'
        self.fontDefault = 'Monaco 12 bold'

        #DATA ATUAL
        self.day = date.today().day
        self.month = date.today().month
        self.year = date.today().year

        #MES CORRENTE PARA PESQUISAS
        self.currentMonth = self.month
        self.currentYear = date.today().year

        #FUNÇÃO DA JANELA PRINCIPAL
        self.viewPrev()

    def viewPrev(self):
        
        self.windowMain = Tk()
        self.windowMain.geometry('680x480+10+10')
        self.windowMain.resizable(False, False)
        self.windowMain.title('FINANCE')

        #VALOR DA CARTEIRA PARA O MÊS
        self.lblCarteira = Label(text='R$ 00,00', font=self.fontStyleUpper, bg=self.verdeClaro, width=30, height=5)
        self.lblCarteira.pack()

        #GASTOS PLANEJADOS
        self.lblGastosPlanejados = Label(text='R$ 00,00', font=self.fontStyleUpper, bg=self.tomato, fg='white', width=12, height=6)
        self.lblGastosPlanejados.pack(side=LEFT)
        
        #DIFERENCA ENTRE A CARTEIRA E OS GASTOS
        self.lblDiferenca = Label(text='R$ 00,00', font=self.fontStyleUpper, bg=self.gold, fg='black', width=15, height=6)
        self.lblDiferenca.pack(side=RIGHT)

        #LABELS DE INFORMAÇÕES
        lblNameCarteira = Label(text='CARTEIRA', font=self.fontDefault, bg=self.verdeClaro)
        lblNameCarteira.place(x=20, y=20)

        lblNameGastos = Label(text='GASTOS DO MÊS', font=self.fontDefault, bg=self.tomato, fg='black')
        lblNameGastos.place(x=20, y=260)

        lblNameGastos = Label(text='SALDO DISPONIVEL', font=self.fontDefault, bg=self.gold, fg='black')
        lblNameGastos.place(x=360, y=260)

        #INICIALIZAR VALORES
        self.setValoresCGD(self.currentMonth, self.currentYear)

        #TECLAS DE FUNCOES
        self.windowMain.bind("<F2>", self.keyPressed)

        self.windowMain.mainloop()

    def keyPressed(self, event):
        l = event.keysym

        #PRESSIONAR F2
        if l == 'F1':
            #TELA DE AJUDA
            pass

        elif l == 'F2':
            #ADICIONAR NOVO GASTO
            pass
        
        elif l == 'F3':
            #ADICIONAR DINHEIRO A CARTEIRA
            pass
        
    def setValoresCGD(self, m, y):

        #PEGAR OS VALORES
        valorCarteira = self.bancoDados.getSaldoCarteira(m, y)
        valorGastos = self.bancoDados.getGastosMes(m, y)
        valorDisponivel = valorCarteira - valorGastos

        #ATRIBUIR O VALOR AS LABELS
        self.lblCarteira['text'] = 'R$ {}'.format(str(valorCarteira).replace('.0', '.00'))
        self.lblGastosPlanejados['text'] = 'R$ {}'.format(str(valorGastos).replace('.0', '.00'))
        self.lblDiferenca['text'] = 'R$ {}'.format(str(valorDisponivel).replace('.0', '.00'))

    def insertValorCarteira(self):
        pass

if __name__ == '__main__':
    financeInterface()