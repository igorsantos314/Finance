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
        self.fontTad = 'Monaco 10 bold'

        #DATA ATUAL
        self.day = date.today().day
        self.month = date.today().month
        self.year = date.today().year

        #MES CORRENTE PARA PESQUISAS
        self.currentMonth = self.month
        self.currentYear = date.today().year

        #LISTA DE CORES DE ACORDO COM O VALOR DE CADA GASTO
        self.colorsValores = ['LightGreen', 'PaleGreen', 'MediumSpringGreen', 'SpringGreen', 'LimeGreen', 'DarkGreen']

        self.tuplaDespesas = (  'CARTÃO',
                                'GASOLINA',
                                'MERCADO',
                                'ALIMENTAÇÃO',
                                'SAUDE',
                                'TECNOLOGIA',
                                'OUTROS')

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

        #SETAR O TITULO DA JANELA
        self.setTitleWindowMain()

        #TECLAS DE FUNCOES
        self.windowMain.bind("<F1>", self.keyPressed)
        self.windowMain.bind("<F2>", self.keyPressed)
        self.windowMain.bind("<F3>", self.keyPressed)
        self.windowMain.bind("<F6>", self.keyPressed)
        self.windowMain.bind("<F8>", self.keyPressed)

        self.windowMain.mainloop()

    def setTitleWindowMain(self):
        #DEFINE O TITULO
        self.windowMain.title(f'FINANCE - {self.currentMonth}/{self.currentYear}')

        #INICIALIZAR VALORES COM BASE NA DATA
        self.setValoresCGD(self.currentMonth, self.currentYear)

    def keyPressed(self, event):
        l = event.keysym

        #PRESSIONAR F2
        if l == 'F1':
            #ADICIONAR VALOR NA CARTEIRA DO MÊS
            self.insertValorCarteira()

        elif l == 'F2':
            #ADICIONAR NOVA DESPESA
            self.insertDespesa()
        
        elif l == 'F3':
            #ADICIONAR DINHEIRO A CARTEIRA
            self.showGastos()
        
        elif l == 'F6':
            #VOLTA UM MES
            self.prevMonth()

        elif l == 'F8':
            #AVANÇA UM MES
            self.nextMonth()

    def nextMonth(self):
            
        #VERIFICA SE ESTA EM DEZEMBRO E AVANÇA UM ANO
        if self.currentMonth == 12:
            self.currentMonth = 1
            self.currentYear += 1
        
        else:
            self.currentMonth += 1

        #ATUALIZA OS VALORES E O TITULO DA JANELA
        self.setTitleWindowMain()

    def prevMonth(self):

        #VERIFICA SE ESTA EM JANEIRO E VOLTA UM ANO ATRAS
        if self.currentMonth == 1:
            self.currentMonth = 12
            self.currentYear -= 1
        
        else:
            self.currentMonth -= 1

        #ATUALIZA OS VALORES E O TITULO DA JANELA
        self.setTitleWindowMain()

    def setValoresCGD(self, m, y):

        #PEGAR OS VALORES
        valorCarteira = self.bancoDados.getSaldoCarteira(m, y)
        valorGastos = self.bancoDados.getGastosMes(m, y)
        valorDisponivel = valorCarteira - valorGastos

        #ATRIBUIR O VALOR AS LABELS
        self.lblCarteira['text'] = 'R$ {}'.format(str(valorCarteira).replace('.0', '.00'))
        self.lblGastosPlanejados['text'] = 'R$ {}'.format(str(valorGastos).replace('.0', '.00'))
        self.lblDiferenca['text'] = 'R$ {}'.format(str(valorDisponivel).replace('.0', '.00'))

    def showGastos(self):

        self.windowShowGastos = Tk()
        self.windowShowGastos.geometry('890x680+10+10')
        self.windowShowGastos.resizable(False, False)
        self.windowShowGastos.title('FINANCE')
        self.windowShowGastos['bg'] = self.gold

        #LINHAS E COLUNAS DO GRID
        r = 0
        c = 0

        for i, g in enumerate(self.bancoDados.getListaGastosMes(self.currentMonth, self.currentYear)):
            
            if i > 27:
                break

            #AO COMPLETAR 4 GASTOS EM UMA LINHA AVANÇA PARA OUTRA
            if i % 4 == 0: 
                c = 0
                r += 1

            #CRIAR O GASTO DO MÊS
            self.createTadGastos(r, c, self.currentMonth, g[0], g[1], g[2], g[3])
            c += 1

        self.windowShowGastos.mainloop()

    def createTadGastos(self, r, c, mes, ind, ano, item, valor):
        
        backGround = 'white'
        foreColor = 'black'

        if valor < 51:
            backGround = self.colorsValores[0]

        elif valor < 101:
            backGround = self.colorsValores[1]

        elif valor < 201:
            backGround = self.colorsValores[1]

        elif valor < 301:
            backGround = self.colorsValores[3]

        elif valor < 501:
            backGround = self.colorsValores[4]
            foreColor = 'white'

        elif valor > 500:
            backGround = self.colorsValores[5]
            foreColor = 'white'

        #print(backGround)

        #CRIA UM BOTÃO PARA GASTO
        lblItem = Button(self.windowShowGastos, text=f'{item[:14]}\nR$ {valor}', font=self.fontTad, bg=backGround, fg=foreColor, width=20, height=4, command=lambda : self.deleteDespesa(ind, mes))
        lblItem.grid(row=r, column=c, pady=5, padx=5)

    def deleteDespesa(self, ind, mes):

        #PERGUNTAR SE DESEJA DELETAR A DESPESA
        if messagebox.askyesno('', f'Deseeja Deletar?') == True:
            self.bancoDados.dropDespesa(mes, ind)

            #MENSAGEM DE SUCESSO
            messagebox.showinfo('', 'Deletado com Sucesso !')

    def insertValorCarteira(self):
        
        self.windowCarteira = Tk()
        self.windowCarteira.geometry('250x160+10+10')
        self.windowCarteira.resizable(False, False)
        self.windowCarteira.title('ADD RECEITA')
        self.windowCarteira['bg'] = self.gold

        #Mes
        lblMes = Label(self.windowCarteira, text='Mês:', bg=self.gold)
        lblMes.place(x=20, y=20)

        comboMes = ttk.Combobox(self.windowCarteira, width = 8) 

        comboMes['values'] = tuple([self.bancoDados.months[i][:3] for i in range(0, 12)])
        comboMes.current(self.month-1)
        comboMes.place(x=20, y=40)

        #Ano
        lblAno = Label(self.windowCarteira, text='Ano:', bg=self.gold)
        lblAno.place(x=130, y=20)

        comboAno = ttk.Combobox(self.windowCarteira, width = 8) 

        comboAno['values'] = tuple(['{}'.format(i) for i in range(2020, 2051)])
        comboAno.current(0)
        comboAno.place(x=130, y=40)

        #VALOR
        lblValor = Label(self.windowCarteira, text='Valor:', bg=self.gold)
        lblValor.place(x=20, y=70)

        etValor = Entry(self.windowCarteira, width=9)
        etValor.place(x=20, y=90)   

        def save():
            #ADICIONAR VALOR A CARTEIRA
            try:
                mes = comboMes.get()
                ano = comboAno.get()
                valor = float(etValor.get())

                self.bancoDados.insertReceita(mes, ano, valor)

                #ATUALIZA E FECHA A JANELA DE RECEITA
                self.setValoresCGD(self.currentMonth, self.currentYear)
                self.windowCarteira.destroy()

                messagebox.showinfo('', 'Receteita Adicionada com Sucesso !')

            except:
                messagebox.showerror('', 'Ocorreu um Erro !')

        #BOTAO SE SALVAMENTO
        btSave = Button(self.windowCarteira, text='SALVAR', bg='MediumSpringGreen', command=save)
        btSave.place(x=130, y=120)

        self.windowCarteira.mainloop()

    def insertDespesa(self):

        self.windowDespesa = Tk()
        self.windowDespesa.geometry('270x170+10+10')
        self.windowDespesa.resizable(False, False)
        self.windowDespesa.title('ADD DESPESA')
        self.windowDespesa['bg'] = self.gold

        #Mes
        lblMes = Label(self.windowDespesa, text='Mês:', bg=self.gold)
        lblMes.place(x=20, y=20)

        comboMes = ttk.Combobox(self.windowDespesa, width= 15) 

        comboMes['values'] = tuple([i for i in range(1, 12)])
        comboMes.current(self.month-1)
        comboMes.place(x=20, y=40)

        #Ano
        lblAno = Label(self.windowDespesa, text='Ano:', bg=self.gold)
        lblAno.place(x=170, y=20)

        comboAno = ttk.Combobox(self.windowDespesa, width = 8) 

        comboAno['values'] = tuple(['{}'.format(i) for i in range(2020, 2051)])
        comboAno.current(0)
        comboAno.place(x=170, y=40)

        #DESPESA
        lblDespesa = Label(self.windowDespesa, text='Tipo de Despesa:', bg=self.gold)
        lblDespesa.place(x=20, y=70)

        comboDespesa = ttk.Combobox(self.windowDespesa, width= 15) 

        comboDespesa['values'] = self.tuplaDespesas
        comboDespesa.current(2)
        comboDespesa.place(x=20, y=90)

        #VALOR
        lblValor = Label(self.windowDespesa, text='Valor:', bg=self.gold)
        lblValor.place(x=170, y=70)

        etValor = Entry(self.windowDespesa, width=9)
        etValor.place(x=170, y=90)

        def save():

            try:
                mes = int(comboMes.get())
                ano = comboAno.get()
                item = comboDespesa.get()
                valor = float(etValor.get())

                self.bancoDados.insertItem(mes, ano, item, valor)

                #MENSAGEM DE SUCESSO
                messagebox.showinfo('', 'Adicionado Com Sucesso !')

                #ATUALIZA OS VALORES E O TITULO DA JANELA
                self.setTitleWindowMain()

            except:
                messagebox.showerror('', 'Ocorreu um Erro !')

        #BOTAO SE SALVAMENTO
        btSave = Button(self.windowDespesa, text='SALVAR', bg='MediumSpringGreen', command=save)
        btSave.place(x=170, y=120)

        self.windowDespesa.mainloop()

if __name__ == '__main__':
    financeInterface()