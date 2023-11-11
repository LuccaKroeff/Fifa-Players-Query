#--------------------------------------------------------------------------------------

# Alunos:
# Lucca Franke Kroeff - 334209
# Sofia de Moraes Sauter Braga - 333496

#---------------------------------------------------------------------------------------

import csv
import re   #utilizado para a leitura dos inputs no nosso código
import time
SIZE_TABELA_HASH_USERS = 24179999


#----------------------------------------------------------------------------------------

# ÁRVORE TRIE

#----------------------------------------------------------------------------------------
class TrieNode:
    def __init__(self, char):
        self.char = char
        self.is_end = False
        self.id = 0
        self.children = {}
        self.positions = ""

class Trie(object):
    def __init__(self):
        self.root = TrieNode("")

    def insert(self, id, word, positions):
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node
        node.is_end = True
        node.id = id
        node.positions = positions
        
    def dfs(self, node, prefix):
        if node.is_end:
            self.output.append((prefix + node.char, node.id, node.positions))
        for child in node.children.values():
            self.dfs(child, prefix + node.char)
        
    def query(self, x):
        self.output = []
        node = self.root
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                return [] 
        self.dfs(node, x[:-1])
        return sorted(self.output, key=lambda x:x[0])

#----------------------------------------------------------------------------------------

# FUNÇÃO DE HASHING

#----------------------------------------------------------------------------------------

def Hashing(id, size):
    StringID = str(id)
    for i in StringID:
        ValorHash = (id * 7) + ord(i)
    ValorHash = ValorHash % size

    return ValorHash

#----------------------------------------------------------------------------------------

# FUNÇÕES DE INICIALIZACAÇÃO

#----------------------------------------------------------------------------------------

# Faz uma Tabela Hash com o hashing do ID do User e coloca na Tabela, também faz o VetorRatingCount que contém respectivamente essas duas informações

def Inicializacao1(reader):
    Tabela = [None] * SIZE_TABELA_HASH_USERS
    VetorRatingCount = [[0, 0]] * 258971
    #ContadorLinhas = 0
    next(reader)
    for i in reader:

        #ContadorLinhas += 1
        #if(ContadorLinhas == 1000000):
          #break
          
        VetorRatingCount[int(i[1])] = CalculaRatingCount(i, VetorRatingCount)    #o formato é [count, sum_rating] 

        ValorHash = Hashing(int(i[0]), SIZE_TABELA_HASH_USERS)       #faz o hash com a id do user
        if(Tabela[ValorHash] == None):
            Tabela[ValorHash] = [i]
        else:
            Tabela[ValorHash].append(i)

    return Tabela, VetorRatingCount

def Inicializacao2(reader):
    VetorGlobalRating = [[-1]] * 18945
    TabelaNomePos = [None] * 23677
    ArvoreJogadores = Trie()
    ContadorLinhas = 0
    next(reader)

    for line in reader:
        ContadorLinhas += 1

        ArvoreJogadores.insert(int(line[0]), line[1], line[2])

        ValorHash = Hashing(int(line[0]), 23677)
        if(TabelaNomePos[ValorHash] == None):
            TabelaNomePos[ValorHash] = [line]
        else:
            TabelaNomePos[ValorHash].append(line)

        Dupla = VetorRatingCount[int(line[0])]
        if(Dupla[0] != 0):
            line[2] = line[2].replace(",","")
            VetorGlobalRating[ContadorLinhas] = [Dupla[1] / Dupla[0], line[0], line[2].split()]
        else: 
            VetorGlobalRating[ContadorLinhas] = [Dupla[1], line[0], line[2].split()]

    return sorted(VetorGlobalRating, reverse=True), TabelaNomePos, ArvoreJogadores

# Faz uma Tabela Hash com o Hashing do ID do jogador e coloca as Tags nessa tabela

def Inicializacao3(reader):
    size = 23677
    VetorTags = [[]] * size
    next(reader)
    for line in reader:
        ValorHash = Hashing(int(line[1]), size)
        if(VetorTags[ValorHash] == []):
            VetorTags[ValorHash] = [[line[2], line[1]]]
        else:
            VetorTags[ValorHash].append([line[2], line[1]])

    return VetorTags

def CalculaRatingCount(i, VetorRatingCount):
    Dupla = [VetorRatingCount[int(i[1])][0], VetorRatingCount[int(i[1])][1]]
    Dupla[1] += float(i[2])
    Dupla[0] += 1
    return Dupla

#----------------------------------------------------------------------------------------

# FUNÇÕES PARA PRINTAR NA TELA 

#----------------------------------------------------------------------------------------

def Display1():
    print("_______________________________________________________________________________________________________________________")
    print("|sofifa_id       name                                         player_positions    rating                   count      |")
    print("|---------------------------------------------------------------------------------------------------------------------|")

def Display2():
    print("_______________________________________________________________________________________________________________________")
    print("|sofifa_id       name                                         global_rating       count                    rating     |")
    print("|---------------------------------------------------------------------------------------------------------------------|")

def DisplayFinal():
    print("|---------------------------------------------------------------------------------------------------------------------|")

def CriaTabela(Dado1, Dado2, Dado3, Dado4, Dado5):
    Dado4 = '{0:.8g}'.format(Dado4)
    print('|' + (f"{Dado1:<6}") + "          " + (f"{Dado2:<45}{Dado3:<20}{Dado4:<25}{Dado5:<11}") + '|')

def CriaTabela2(Dado1, Dado2, Dado3, Dado4, Dado5):
    Dado3 = '{0:.8g}'.format(Dado3)
    print('|' + (f"{Dado1:<6}") + "          " + (f"{Dado2:<45}{Dado3:<20}{Dado4:<25}{Dado5:<11}") + '|')

#----------------------------------------------------------------------------------------

# FUNÇÕES PARA RETORNAR NOME E POSIÇÃO DO JOGADOR CONSULTANDO A TABELA HASH

#----------------------------------------------------------------------------------------

def GetName(ID):
    ValorH = Hashing(int(ID), 23677)   
    for k in TabelaNomePos[ValorH]:
        if(int(k[0]) == int(ID)):
            return k[1]

def GetPos(ID):
    ValorHash = Hashing(int(ID), 23677)
    for i in TabelaNomePos[ValorHash]:
        if(int(i[0]) == int(ID)):
            return i[2]
        
#----------------------------------------------------------------------------------------

# FUNÇÃO 1: BUSCAR NOME JOGADORES 

#----------------------------------------------------------------------------------------
def BuscarNomeJogadores():
    Pesquisa = re.search('player (.*)', Search)
    JogadorPesquisado = Pesquisa.group(1)
    ResultadoBusca = ArvoreJogadores.query(JogadorPesquisado)
    Display1()

    for Jogador in ResultadoBusca:
            dupla_tabela = VetorRatingCount[Jogador[1]]
            if(dupla_tabela[1] == 0):
                CriaTabela(str(Jogador[1]), Jogador[0], Jogador[2], dupla_tabela[0], str(dupla_tabela[1]))
            else:
                CriaTabela(str(Jogador[1]), Jogador[0], Jogador[2], dupla_tabela[1] / dupla_tabela[0], str(dupla_tabela[0]))
    DisplayFinal()      
            
#----------------------------------------------------------------------------------------

# FUNÇÃO 2: BUSCAR POR AVALIAÇÕES DE USUÁRIOS 

#----------------------------------------------------------------------------------------
def BuscarUsuario():
    Pesquisa = re.search('user (.*)', Search)
    UserPesquisado = int(Pesquisa.group(1))
    Contador = 0    #Indicará se já escrevemos 20 reviews
    Display2()
    ValorHash = Hashing(int(UserPesquisado), SIZE_TABELA_HASH_USERS)
    if(TabelaHash[ValorHash] == None):
        DisplayFinal()
    else:
        TabelaHash[ValorHash] = sorted(TabelaHash[ValorHash], key=lambda x: x[2], reverse=True)

        for i in TabelaHash[ValorHash]:
            if(Contador > 20):
                break
            if(int(i[0]) == int(UserPesquisado)):
                Dupla = VetorRatingCount[int(i[1])]
                NomeJogador = GetName(i[1])
                CriaTabela2((i[1]), NomeJogador, Dupla[1] / Dupla[0], Dupla[0], i[2])
                Contador += 1
        DisplayFinal()

#----------------------------------------------------------------------------------------

# FUNÇÃO 3: MELHORES JOGADORES DE UMA POSIÇÃO

#----------------------------------------------------------------------------------------
def BuscarJogadoresPosicao():
    Pesquisa = re.search('top(.*) (.*)', Search)
    PosicaoPesquisada = (Pesquisa.group(2)).upper()
    Numero = int(Pesquisa.group(1))
    Contador = -1
    ContadorLaco = 0
    Display1()

    while((ContadorLaco != Numero)):
        Contador += 1
        if(Contador == 18945):
            break
        Jogador = VetorGlobalRating[Contador]
        if(Jogador == [-1]):
            pass
        else:
            for Posicao in Jogador[2]:
                Dupla = VetorRatingCount[int(Jogador[1])]
                if(Dupla[0] > 1000):
                    if(Posicao == PosicaoPesquisada):
                        NomeJogador = GetName(Jogador[1])
                        CriaTabela(Jogador[1], NomeJogador, ', '.join(Jogador[2]), Jogador[0], Dupla[0])
                        ContadorLaco += 1
    DisplayFinal()

#----------------------------------------------------------------------------------------

# FUNÇÃO 4: PESQUISA SOBRE TAGS DE JOGADORES 

#----------------------------------------------------------------------------------------
def BuscarTagsJogadores():
    Search.replace(' ', '')
    Pesquisa = re.search('tags(.*)', Search)
    TagsPesquisadas = (Pesquisa.group(1)).split("'")   #pega todas as tags e separa em uma lista de Tags
    TagsPesquisadas.remove('')
    TagsPesquisadas = list(set(TagsPesquisadas))    #função set retira todas os elementos repetidos da lista
    TagsPesquisadas.remove(' ')
    vetor_jogadores = []
    jogadores_real = []
    jogadores_total = []
    #VetorTags = [[['B', '33'], ['D', '33'], ['C', '33'], ['C', '37'], ['D', '37'], ['F', '42'], ['B', '42']], [['B', '38'], ['D', '35'], ['C', '35'], ['C', '38'], ['D', '38'], ['F', '42'], ['B', '41']]]
    Display1()

    for Jogador in VetorTags:
        valor = -1
        if(Jogador == []):
            pass
        else:
            for elemento in TagsPesquisadas:
                valor += 1
                for i in Jogador:
                    if(i[0] == elemento):
                        if(valor > 0):
                            for j in vetor_jogadores:
                                if(i[1] == j):
                                    jogadores_real.append(j)
                                    break
                        else:
                            if(vetor_jogadores == []):
                                vetor_jogadores.append(i[1])
                            elif(vetor_jogadores[-1] != i[1]):
                                vetor_jogadores.append(i[1])  
                if(valor > 0):
                    vetor_jogadores = jogadores_real
                    jogadores_real = []      

                if(vetor_jogadores == []):
                    break

            for i in vetor_jogadores:
                jogadores_total.append(i)

        vetor_jogadores = []
    jogadores_total = list(set(jogadores_total))

    for i in jogadores_total:
        Dupla = VetorRatingCount[int(i)]
        NomeJogador = GetName(i)
        PosicaoJogador = GetPos(i)
        if(Dupla[0] != 0):
            CriaTabela(i, NomeJogador, PosicaoJogador, Dupla[1] / Dupla[0], Dupla[0])
        else:
            CriaTabela(i, NomeJogador, PosicaoJogador, Dupla[1], Dupla[0])
    DisplayFinal()
        
#----------------------------------------------------------------------------------------
 
# PRÉ PROCESSAMENTO                         

#----------------------------------------------------------------------------------------
start = time.time()

with open(r"C:\Users\lucca\Desktop\Trabalho Final - CPD\rating.csv") as ArquivoAvaliacoes:
    reader = csv.reader(ArquivoAvaliacoes)
    TabelaHash, VetorRatingCount = Inicializacao1(reader)   #manda o id do jogador para a função de inserir hash na tabela

with open(r"C:\Users\lucca\Desktop\Trabalho Final - CPD\players.csv") as ArquivoJogadores:
    reader = csv.reader(ArquivoJogadores)
    VetorGlobalRating, TabelaNomePos, ArvoreJogadores = Inicializacao2(reader)

with open(r"C:\Users\lucca\Desktop\Trabalho Final - CPD\tags.csv") as ArquivoTags:
        reader = csv.reader(ArquivoTags)
        VetorTags = Inicializacao3(reader)

end = time.time()
tempo = end - start
print("O tempo de pré processamento foi de: {:.3f} segundos".format(tempo))
#----------------------------------------------------------------------------------------
 
# CÓDIGO MAIN                                

#----------------------------------------------------------------------------------------

Search = '1'
while(Search != '0'):
    Search = input("$ ")
    if(Search[0:6] == 'player'):
        BuscarNomeJogadores()
    elif(Search[0:4] == 'user'):
        BuscarUsuario()
    elif(Search[0:3] == 'top'):
        Search = Search.replace("'", '')
        BuscarJogadoresPosicao()
    elif(Search[0:4] ==  'tags'):
        BuscarTagsJogadores()