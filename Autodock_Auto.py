#!/usr/bin/env python
# coding: utf-8

# In[2]:


#inicialmente aplicamos as bibliotecas que iremos utilizar.
#Blibiotecas de Plotagem de dados e gráficos.
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import pandas as pd
#Blibiotecas de acesso ao sistemas
import subprocess
import sys
import os
from subprocess import Popen


# In[43]:


def Coordenadas (arquivo):
    l, cont = 0, True
    x, y, z = [], [], []
    while cont == True:
        if arquivo[l] == "MODEL 1\n":
            while arquivo[l] != "MODEL 2\n":
                linha = arquivo[l].split()
                if linha[0] == "ATOM":
                    x.append(float(linha[5]))
                    y.append(float(linha[6]))
                    z.append(float(linha[7]))
                if linha[0] == "HETATM":
                    x.append(float(linha[4]))
                    y.append(float(linha[5]))
                    z.append(float(linha[6]))
                l = l + 1
        if arquivo[l] == "MODEL 2\n":
            cont = False
        l = l + 1
        
    x_novo = sum(x)/len(x)
    y_novo = sum(y)/len(y)
    z_novo = sum(z)/len(z)
    with open('Movimentação.txt', 'a') as grafico:
        grafico.write(f'{x_novo} {y_novo} {z_novo}\n')
    return [x_novo, y_novo, z_novo]

def Conf(receptor, ligand, out, x, y, z, cx, cy, cz, exh):
    with open("conf.txt", "w") as arquivo:
        arquivo.write(f'receptor = {receptor}.pdbqt\n'
                      f'ligand = {ligand}.pdbqt\n'
                      f'\n'
                      f'out = {out}.pdbqt\n'
                      f'\n'
                      f'center_x = {x}\n'
                      f'center_y = {y}\n'
                      f'center_z = {z}\n'
                      f'\n'
                      f'size_x = {cx}\n'
                      f'size_y = {cy}\n'
                      f'size_z = {cz}\n'
                      f'\n'
                      f'exhaustiveness = {exh}')
    return

#Para tanto notamos que a informação log, é perdida durantye o processo de execução, precisamos de um arquivo de saída que nos de todas as informações para nossa analise
def Informação(receptor, ligand, out, x, y, z, cx, cy, cz, exh):
    with open("Informações.txt", "a") as arquivo:
        arquivo.write(f'Ligante: {ligand}\n'
                      f'Receptor: {receptor}\n'
                      f'Nome de Saída: {out}\n' 
                      f'Posição do centro da caixa: ({x},{y},{y})\n'
                      f'Dimensões da caixa: {cx} p/ eixo x, {cy} p/ eixo y, {cz} p/ eixo z\n'
                      f'exhaustiveness: {exh}\n'
                      f'\n'
                      f'\n')
    return

def Energias(Nome):
    arquivo = list(open(f"{Nome}.txt", 'r'))
    dentro = True
    l = 0
    while dentro == True:
        linha_parcela = arquivo[l].split()
        if len(linha_parcela) != 0:
            if linha_parcela[0] == "mode":
                veri = True
                while veri == True:
                    with open("Informações.txt", "a") as informacao:
                        informacao.write(arquivo[l])
                    linha_parcela2 = arquivo[l + 1].split()
                    if linha_parcela2[0] == 'Writing':
                        veri = False
                        dentro = False
                    l += 1
        l += 1
    with open("Informações.txt", "a") as informacao:
        informacao.write('\n')
    return


# In[ ]:


#Nome dos arquivos
print("insira o nome do arquivo do receptor")
receptor = str(input())
print("insira o nome do arquivo do ligante")
ligand = str(input())
print("Nome dpo arquivo de saida")
out = str(input())
print("O numero de passos")
passos = int(input())
print("insira o tamanho de cada eixo da caixa")
print("tamanho x:")
cx = int(input())
print("tamanho y:")
cy = int(input())
print("tamanho z:")
cz = int(input())
print("insira o exhaustiveness")
exh = int(input())


# In[1]:


p = 0
while p <= passos:
    arquivo = open(f'{out}.pdbqt',"r")
    centro_caixa = Coordenadas(list(arquivo))
    out = "res_out" + f"{p}"
    Informação(receptor, ligand, out, centro_caixa[0], centro_caixa[1], centro_caixa[2], cx, cy, cz, exh)
    Conf(receptor, ligand, out , centro_caixa[0], centro_caixa[1], centro_caixa[2], cx, cy, cz, exh)
    
    try:
        c3 = os.system('vina --config conf.txt --log log.txt')
    except Exception as E:
        print('Não foi possivel rodar o docking, por favor verifique o seguinte comando de erro')
        ERRO(E)
        exit()
    Energias('log')
    
    try:
        c3 = os.system(f'vina_split --input {out}.pdbqt')
    except Exception as E:
        print('Não foi possivel rodar o docking, por favor verifique o seguinte comando de erro')
        ERRO(E)
        exit()
    
    try:
        c3 = os.system('clear')
    except Exception as E:
        print('Não foi possivel rodar o docking, por favor verifique o seguinte comando de erro')
        ERRO(E)
        exit()
    p += 1
exit()


# In[ ]:





# In[37]:





# In[ ]:





# In[ ]:




