import random
import json


class Jogador:

    def __init__(self, nome):
        self.nome = nome
        self.pontos = 0
        self.recursos = {"madeira": 0, "tijolo": 0, "trigo": 0, "minerio": 0}

    def tem_recursos(self, custo):
        for r in custo:
            if self.recursos[r] < custo[r]:
                return False
        return True

    def pagar(self, custo):
        for r in custo:
            self.recursos[r] -= custo[r]

    def para_dicionario(self):
        return {"nome": self.nome, "pontos": self.pontos, "recursos": self.recursos}


class Terreno:

    def __init__(self, id, recurso, numero):
        self.id = id
        self.recurso = recurso
        self.numero = numero
        self.edificio = ""
        self.dono = ""
        self.estrada = ""

    def esta_vazio(self):
        return self.edificio == "" and self.estrada == ""

    def para_dicionario(self):
        return {"id": self.id, "recurso": self.recurso, "numero": self.numero,
                "edificio": self.edificio, "dono": self.dono, "estrada": self.estrada}


class Jogo:

    RECURSOS = ["madeira", "tijolo", "trigo", "minerio"]
    CUSTO_ESTRADA = {"madeira": 1, "tijolo": 1}
    CUSTO_ALDEIA = {"madeira": 1, "tijolo": 1, "trigo": 1}
    CUSTO_CIDADE = {"trigo": 2, "minerio": 2}

    def __init__(self):
        self.jogadores = []
        self.terrenos = []
        self.iniciado = False
        self.terminado = False
        self.atual = 0
        self.dados = False
        self.historico = []
        self.criar_tabuleiro()

    def criar_tabuleiro(self):
        tab = [["madeira", 5], ["tijolo", 6], ["trigo", 8], ["minerio", 9],
               ["trigo", 4], ["madeira", 10], ["tijolo", 3], ["minerio", 11],
               ["madeira", 6], ["trigo", 8], ["tijolo", 10], ["minerio", 5]]
        for i in range(12):
            self.terrenos.append(Terreno(i + 1, tab[i][0], tab[i][1]))

    def jogador_atual(self):
        return self.jogadores[self.atual]

    def procurar_jogador(self, nome):
        for j in self.jogadores:
            if j.nome.lower() == nome.lower():
                return j
        return None

    def vizinhos(self, n):
        v = []
        if n > 4:
            v.append(n - 4)
        if n < 9:
            v.append(n + 4)
        if n % 4 != 1:
            v.append(n - 1)
        if n % 4 != 0:
            v.append(n + 1)
        return v

    def pode_jogar(self):
        if not self.iniciado:
            return "O jogo ainda não começou."
        if self.terminado:
            return "O jogo já terminou."
        if not self.dados:
            return "Tem de lançar os dados primeiro (LD)."
        return ""

    def verificar_vitoria(self, j):
        if j.pontos >= 5:
            self.terminado = True
            return "\n" + j.nome + " ganhou o jogo!"
        return ""

    def registar(self, nome):
        if nome == "":
            return "O nome não pode estar vazio."
        if self.iniciado:
            return "O jogo já começou."
        if len(self.jogadores) == 4:
            return "Já existem 4 jogadores."
        if self.procurar_jogador(nome) != None:
            return "Jogador já existe."
        self.jogadores.append(Jogador(nome))
        self.historico.append("registou " + nome)
        return "Jogador registado com sucesso."

    def pode_iniciar(self):
        if self.iniciado:
            return "O jogo já foi iniciado."
        if len(self.jogadores) < 2:
            return "São precisos pelo menos 2 jogadores."
        return ""

    def iniciar(self, escolhas):
        for t in escolhas:
            if t < 1 or t > 12:
                return "Terreno inválido."
            if escolhas.count(t) > 1:
                return "As aldeias iniciais devem ocupar terrenos diferentes."
        for i in range(len(escolhas)):
            j = self.jogadores[i]
            terreno = self.terrenos[escolhas[i] - 1]
            terreno.edificio = "aldeia"
            terreno.dono = j.nome
            j.pontos = 1
            j.recursos = {"madeira": 2, "tijolo": 2, "trigo": 2, "minerio": 1}
        self.iniciado = True
        self.historico.append("jogo iniciado")
        return "Jogo iniciado com sucesso."

    def lancar_dados(self):
        if not self.iniciado:
            return "O jogo ainda não começou."
        if self.terminado:
            return "O jogo já terminou."
        if self.dados:
            return "Os dados já foram lançados neste turno."
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        soma = d1 + d2
        self.dados = True
        self.historico.append(self.jogador_atual().nome + " tirou " + str(soma))
        msg = "Dados: " + str(d1) + " + " + str(d2) + " = " + str(soma)
        if soma == 7:
            return msg + "\nO 7 não dá recursos."
        for j in self.jogadores:
            recebeu = {}
            for t in self.terrenos:
                if t.numero == soma and t.dono == j.nome:
                    qtd = 1
                    if t.edificio == "cidade":
                        qtd = 2
                    j.recursos[t.recurso] += qtd
                    if t.recurso in recebeu:
                        recebeu[t.recurso] += qtd
                    else:
                        recebeu[t.recurso] = qtd
            if recebeu != {}:
                msg = msg + "\n" + j.nome + " recebeu: " + str(recebeu)
        return msg

    def construir_estrada(self, n):
        erro = self.pode_jogar()
        if erro != "":
            return erro
        if n < 1 or n > 12:
            return "Terreno inválido."
        j = self.jogador_atual()
        t = self.terrenos[n - 1]
        if not t.esta_vazio():
            return "O terreno já está ocupado."
        perto = False
        for v in self.vizinhos(n):
            if self.terrenos[v - 1].estrada == j.nome or self.terrenos[v - 1].dono == j.nome:
                perto = True
        if not perto:
            return "A estrada deve ficar adjacente a uma construção sua."
        if not j.tem_recursos(self.CUSTO_ESTRADA):
            return "Recursos insuficientes."
        j.pagar(self.CUSTO_ESTRADA)
        t.estrada = j.nome
        self.historico.append(j.nome + " fez estrada no " + str(n))
        return "Estrada construída com sucesso."

    def construir_aldeia(self, n):
        erro = self.pode_jogar()
        if erro != "":
            return erro
        if n < 1 or n > 12:
            return "Terreno inválido."
        j = self.jogador_atual()
        t = self.terrenos[n - 1]
        if t.edificio != "":
            return "Já existe um edifício neste terreno."
        if t.estrada != j.nome:
            return "Tem de construir primeiro uma estrada sua neste terreno."
        if not j.tem_recursos(self.CUSTO_ALDEIA):
            return "Recursos insuficientes."
        j.pagar(self.CUSTO_ALDEIA)
        t.edificio = "aldeia"
        t.dono = j.nome
        j.pontos += 1
        self.historico.append(j.nome + " fez aldeia no " + str(n))
        return "Aldeia construída com sucesso." + self.verificar_vitoria(j)

    def construir_cidade(self, n):
        erro = self.pode_jogar()
        if erro != "":
            return erro
        if n < 1 or n > 12:
            return "Terreno inválido."
        j = self.jogador_atual()
        t = self.terrenos[n - 1]
        if t.dono != j.nome or t.edificio != "aldeia":
            return "Só pode melhorar uma aldeia sua para cidade."
        if not j.tem_recursos(self.CUSTO_CIDADE):
            return "Recursos insuficientes."
        j.pagar(self.CUSTO_CIDADE)
        t.edificio = "cidade"
        j.pontos += 1
        self.historico.append(j.nome + " fez cidade no " + str(n))
        return "Cidade construída com sucesso." + self.verificar_vitoria(j)

    def trocar(self, dar, receber):
        erro = self.pode_jogar()
        if erro != "":
            return erro
        if dar not in self.RECURSOS or receber not in self.RECURSOS or dar == receber:
            return "Recursos inválidos: escolha dois recursos diferentes."
        j = self.jogador_atual()
        if j.recursos[dar] < 3:
            return "Recursos insuficientes."
        j.recursos[dar] -= 3
        j.recursos[receber] += 1
        self.historico.append(j.nome + " trocou " + dar + " por " + receber)
        return "Troca realizada com sucesso."

    def finalizar_turno(self):
        if not self.iniciado:
            return "O jogo ainda não começou."
        if self.terminado:
            return "O jogo já terminou."
        if not self.dados:
            return "Tem de lançar os dados primeiro (LD)."
        self.atual += 1
        if self.atual == len(self.jogadores):
            self.atual = 0
        self.dados = False
        return "Turno terminado. Agora joga " + self.jogador_atual().nome + "."

    def gravar(self, nome):
        if nome == "":
            return "O nome do ficheiro nao pode estar vazio."
        lista_jogadores = []
        for j in self.jogadores:
            lista_jogadores.append(j.para_dicionario())
        lista_terrenos = []
        for t in self.terrenos:
            lista_terrenos.append(t.para_dicionario())
        dados = {"jogadores": lista_jogadores, "terrenos": lista_terrenos,
                 "iniciado": self.iniciado, "terminado": self.terminado,
                 "atual": self.atual, "dados": self.dados, "historico": self.historico}
        try:
            f = open(nome, "w")
            json.dump(dados, f)
            f.close()
        except:
            return "Erro ao gravar o ficheiro."
        return "Jogo gravado com sucesso."

    def ler(self, nome):
        if nome == "":
            return "O nome do ficheiro nao pode estar vazio."
        try:
            f = open(nome, "r")
            dados = json.load(f)
            f.close()
        except FileNotFoundError:
            return "Erro: o ficheiro não existe."
        except:
            return "Ficheiro de jogo inválido ou danificado."
        try:
            jogadores = []
            for d in dados["jogadores"]:
                j = Jogador(d["nome"])
                j.pontos = d["pontos"]
                j.recursos = d["recursos"]
                jogadores.append(j)
            terrenos = []
            for d in dados["terrenos"]:
                t = Terreno(d["id"], d["recurso"], d["numero"])
                t.edificio = d["edificio"]
                t.dono = d["dono"]
                t.estrada = d["estrada"]
                terrenos.append(t)
            if len(terrenos) != 12:
                return "Ficheiro de jogo inválido ou danificado."
            self.iniciado = dados["iniciado"]
            self.terminado = dados["terminado"]
            self.atual = dados["atual"]
            self.dados = dados["dados"]
            self.historico = dados["historico"]
        except:
            return "Ficheiro de jogo inválido ou danificado."
        self.jogadores = jogadores
        self.terrenos = terrenos
        return "Jogo carregado com sucesso."
