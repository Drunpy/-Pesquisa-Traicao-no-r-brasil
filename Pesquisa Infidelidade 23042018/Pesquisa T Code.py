'''
        Para o r/brasil

        Pesquisa, análise e gráficos por:
        u/Drunpy

            • Estrutura do código:
                • Apresentação
                • Imports
                • Separação dos dados
                • Gráficos
            
'''

    #IMPORTS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

pesquisa = pd.read_csv("Pesquisa T.csv")
df = pd.DataFrame(pesquisa)

    #SEPARAÇÃO DOS DADOS

#Renomeando as colunas para facilitar a leitura
df.columns = ["data", "estado", "idade", "sexo", "renda", "estadocivil", "jatraiu", "jafoitraido", "comoseusamigosencaramisso", "comovcencaraisso", "nafamilia", "qmtraimais", "Sugestoesoucomentarios"]

#Lista com todos os estado para serem usados na separação dos dados
estadosunico = ['MG', 'SC', 'RS', 'SP', 'RJ', 'PE', 'GO', 'DF', 'BA', 'CE', 'PR', 'AL', 'ES', 'RN', 'SE', 'PB', 'TO', 'PI', 'PA', 'RO', 'MT', 'MA', 'AM', 'RR', 'MS', 'AP']

#Abaixo todos os códigos tem intenção de filtrar os dados

estado_x_pessoas = {}
estados_validos = {}

for i in estadosunico:
    qnt = np.count_nonzero(df.estado == i)
    estado_x_pessoas[i] = int(qnt)

#Quantidade de participantes >=19 para o estado ser válido  
for k,v in estado_x_pessoas.items():
    if v >= 19:
        estados_validos[k] = v

#Separando qnt de traidores(pessoas) por estado                              
estado_x_jatraiu = {}
for i in estados_validos:
    qntjatraiu = np.count_nonzero((df.estado == i) & (df.jatraiu == 'Não'))
    estado_x_jatraiu[i] = int(qntjatraiu)


#Extraindo opcoes de idade
idadeops = []
for i in df.idade:
    if i not in idadeops:
        idadeops.append(i)
#correlacionando idades + traidores
idade_traiuqnt = {}
for i in idadeops:
    qntraidores = np.count_nonzero((df.idade == i) & (df.jatraiu == 'Sim'))
    idade_traiuqnt[i] = int(qntraidores)

#Total de pessoas por idade
total_poridade = {}
for i in idadeops:
    cont = np.count_nonzero(df.idade == i)
    total_poridade[i] = cont

#Correlacionando participantes e renda
rendas_un = []
total_prenda ={}
for i in df.renda:
    if i not in rendas_un:
        rendas_un.append(i)

#^GAMBIARRA para trocar o nome do Xticks no gráfico
total_prenda = {'<1000': 78, 'Entre 1000 e 2000': 71, '8000+': 46, 'Entre 3000 e 5000': 49, 'Entre 2000 e 3000': 46, 'Entre 5000 e 8000': 28}

#Quem trai mais
traimais = {'Mulher': 0 , 'Homem': 0}
for i in df.qmtraimais:
    mulher = np.count_nonzero(df.qmtraimais == 'Mulher')
    homem = np.count_nonzero(df.qmtraimais == 'Homem')
    traimais['Mulher'] = mulher
    traimais['Homem'] = homem

#Correlação sexo + Trai (qual dos sexos traiu mais)
sexo_traicao_sim = {}
for i in df.sexo:
    ses = np.count_nonzero((df.sexo == i) & (df.jatraiu == 'Sim'))
    if ses != 0:
        sexo_traicao_sim[i] = ses 

sexo_traicao_nao ={}
for i in df.sexo:
    sen = np.count_nonzero((df.sexo == i) & (df.jatraiu == 'Não'))
    if sen != 0:
        sexo_traicao_nao[i] = sen

#O que você acha sobre traicao ?
opn_g = {}
for i in df.comovcencaraisso:
    como = np.count_nonzero(df.comovcencaraisso == i)
    opn_g[i] = como

'''
    #Muitos dados para um intel pentium... SKIPED
#Correl sexo/jafoitraido
sexo_jafoitraido = {}
for sexo in df.sexo:
    for i in df.jafoitraido:
        jafoi = np.count_nonzero((df.sexo == sexo) & (df.jafoitraido == i))
        if jafoi != 0:
            sexo_jafoitraido[sexo] = jafoi
'''

    #GRAFICOS   
def total_pessoas():
    exp = pd.DataFrame.from_dict(estados_validos, orient='index')

    exp.plot(kind='pie',
             subplots=True,
             shadow=True,
             explode=[0,0 ,0.05 ,0 , 0],
             labeldistance=1.1,
             autopct='%.1f%%')

    plt.title('Participações validadas', fontsize=15)
    plt.suptitle('Não foram obtidos dados significativos\n de outros estados.', y=0.88, fontsize=6)
    plt.show()

def mulhertraida():
    dfmulhertraida = pd.DataFrame.from_dict(sexo_jafoitraido, orient='index')
    

def opn_geral():
    dfopng = pd.DataFrame.from_dict(opn_g, orient='index')

    dfopng.plot(kind='pie',
                subplots=True,
                shadow=True,
                explode=[0.05, 0 ,0 ,0 , 0],
                autopct = '%.1f%%')

    plt.title('O que as pessoas acham sobre traição ?', size=20)
    plt.suptitle('**Do total de respostas.', y=0.88, size=12)
    plt.show()

def sexotraicaosim():
    dfsts = pd.DataFrame.from_dict(sexo_traicao_sim, orient='index')

    dfsts.plot(kind='pie',
               subplots=True,
               shadow=True,
               explode= [0, 0.1, 0,0],
               autopct='%.1f%%')

    plt.title('Os que já trairam são: ', size=20)
    plt.suptitle('**Ou opção sexual', y=0.88, size=9)
    plt.show()

def traidores_estado():
    dfestadosvalidos = pd.DataFrame.from_dict(estados_validos, orient='index')
    dfestadosvalidos.columns = ['estado']
    dfestado = pd.DataFrame.from_dict(estado_x_jatraiu, orient='index')
    dfestado.columns = ['estado']

    ax = dfestadosvalidos.plot(color='#3366ff',
                               kind='bar',
                               zorder=2)

    dfestado.plot(kind='bar',
                  ax=ax,
                  label=True,
                  color='#ff3333',
                  title="Participantes que já trairam, por estado.",
                  zorder=2).legend(['Total','Já trairam'])

    plt.xticks(rotation=0)
    plt.grid(axis='y')
    plt.xlabel("Estado")
    plt.ylabel("Participantes")
    plt.show()

def participantes_estado():
    
    x_axis = ['MG', 'SC', 'SP', 'RJ', 'PR']
    y_axis = estados_validos.values()

    ind = np.arange(len(y_axis))

    plt.title("Quantidade de participantes por estado")

    plt.bar(ind, y_axis, align='center')
    plt.xticks(ind, x_axis)      
    plt.grid('on', axis='y')
    plt.show()

def traicao_idade():
    x_axis = total_poridade.values()
    y_axis = total_poridade.keys()
    x2_axis =  idade_traiuqnt.values()

    ind = np.arange(len(y_axis))
    ind_inverted = np.arange(len(y_axis))[::-1]
    
    plt.barh(ind-0.3,
             list(x_axis)[::-1],
             height=-0.3,
             align='center',
             zorder=2)

    plt.barh(ind-0.6,
             list(x2_axis)[::-1],
             height=-0.3,
             align='center')

    plt.yticks(ind_inverted-0.45, y_axis)
    plt.grid('on', axis='x')
    plt.xlabel('Participantes')
    plt.ylabel('Faixa etária')
    plt.legend(('Total por idade','Já trairam'), loc=1)
    plt.title('Traição por faixa etária', fontsize=20) 
    plt.show()

def traicao_renda():
    dfrenda = pd.DataFrame.from_dict(total_prenda, orient='index')
    dfrenda.columns = ['total']
    dfrenda.set_index(dfrenda.columns[0])

    dfrenda.plot(kind='bar',
                 rot=60,
                 width=1,
                 zorder=2,
                 legend=False,
                 color=[plt.cm.Paired(np.arange(len(dfrenda)))])

    plt.grid('on', axis='y')
    plt.ylabel('Total', fontsize=15)
    plt.title('Traição por renda mensal', fontsize=20)
    plt.show()
  
def qmtraimais():
    dftraimais = pd.DataFrame.from_dict(traimais, orient='index')

    dftraimais.plot(kind='pie',
                    shadow=True,
                    explode=[0, 0.1],
                    subplots=True,
                    autopct='%.1f%%')

    plt.title('Quem trai mais ?', fontsize=20)
    plt.show()

