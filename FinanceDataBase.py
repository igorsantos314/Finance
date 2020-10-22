import sqlite3
import os
from random import sample

class bd:

    def __init__(self):

        #LISTA DE MESES
        self.months = ['JANEIRO', 'FEVEREIRO', 'MARCO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']

        caminhoAtual = os.getcwd()
        print(caminhoAtual)

        self.conection = sqlite3.connect('{}/finance.db'.format(caminhoAtual))
        self.cur = self.conection.cursor()

    def createTablesMonths(self, m):
        #CRIAR TABELAS DE MESES
        command = 'CREATE TABLE {} (ano TEXT, Item TEXT, valor REAL)'.format(m)
        
        self.cur.execute(command)
        self.conection.commit()
        
    def createTableCarteira(self):
        #CRIAR TABELA CARTEIRA
        command = 'CREATE TABLE CARTEIRA (mes TEXT, ano TEXT, valor REAL)'
        
        self.cur.execute(command)
        self.conection.commit()

    def insertItem(self, m, ano, Item, valor):

        #INSERIR DADOS NA TABELA MES NA POSICAO M
        command = f'INSERT INTO {m} (ano, Item, valor) VALUES("{ano}", "{Item}", {valor})'
        
        self.cur.execute(command)
        self.conection.commit()

    def insertReceita(self, m, ano, valor):
        #INSERIR DADOS NA TABELA CARTEIRA
        command = f'INSERT INTO CARTEIRA (mes, ano, valor) VALUES("{m}", "{ano}", {valor})'
        
        self.cur.execute(command)
        self.conection.commit()

    def getGastosMes(self, m, y):
        
        #TRANSFORMA MES DE NUMERO PARA O NOME
        m = self.months[m-1]

        #EXIBIR TODOS OS DADOS DE UMA TABELA MES, PELA DATA ESPECIFICA
        show = f"SELECT valor FROM {m} WHERE ano = '{y}'"

        self.cur.execute(show)
        valores = self.cur.fetchall()

        #RETORNA A SOMA DOS VALORES DO MES E ANO DESEJADOS
        return sum([v[0] for v in valores])

    def getSaldoCarteira(self, m, y):

        #TRANSFORMA MES DE NUMERO PARA O NOME
        m = self.months[m-1]

        #EXIBIR TODOS OS DADOS DE UMA TABELA MES, PELA DATA ESPECIFICA
        show = f"SELECT valor FROM CARTEIRA WHERE ano = '{y}' AND mes = '{m}'"

        self.cur.execute(show)
        valores = self.cur.fetchall()

        #RETORNA A SOMA DOS VALORES DO MES E ANO DESEJADOS
        return sum([v[0] for v in valores])

    def getListaGastosMes(self, m, y):
        
        #TRANSFORMA MES DE NUMERO PARA O NOME
        m = self.months[m-1]

        #EXIBIR TODOS OS DADOS DE UMA TABELA MES, PELA DATA ESPECIFICA
        show = f"SELECT * FROM {m} WHERE ano = '{y}'"

        self.cur.execute(show)
        gastos = self.cur.fetchall()

        #RETORNA A SOMA DOS VALORES DO MES E ANO DESEJADOS
        return gastos

a = bd()
#print(a.getListaGastosMes(10, 2020))
#print(a.getSaldoCarteira(1, '2020'))
#a.insertReceita('OUTUBRO', '2020', '500')
#a.createTableCarteira()
#for i in sample([i for i in range(1000)], 27):
#    a.insertItem('OUTUBRO', '2020', 'ALGUMA COISA', i)
#for i in a.months:
#    a.createTablesMonths(i)
