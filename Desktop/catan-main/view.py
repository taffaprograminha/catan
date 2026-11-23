VERMELHO = "\033[91m"
VERDE = "\033[92m"
AMARELO = "\033[93m"
AZUL = "\033[96m"
NORMAL = "\033[0m"


class View:

    def mostrar_menu(self):
        print(AZUL)
        print("RJ - Registar Jogador   IJ - Iniciar Jogo     LD - Lançar Dados")
        print("CE - Construir Estrada  CA - Construir Aldeia CC - Construir Cidade")
        print("TR - Trocar Recursos    FT - Finalizar Turno  G - Gravar   L - Ler")
        print("VT - Ver Tabuleiro      EE - Estado do Jogo   AJ - Ajuda   S - Sair" + NORMAL)

    def pedir(self, texto):
        return input(texto)

    def mostrar_mensagem(self, texto):
        if "ganhou" in texto:
            print(AMARELO + texto + NORMAL)
        elif "sucesso" in texto or "Turno terminado" in texto:
            print(VERDE + texto + NORMAL)
        elif texto.startswith("Dados"):
            print(AMARELO + texto + NORMAL)
        else:
            print(VERMELHO + texto + NORMAL)

    def mostrar_tabuleiro(self, terrenos):
        for t in terrenos:
            linha = str(t.id) + " " + t.recurso + " (" + str(t.numero) + ")"
            if t.edificio != "":
                linha = linha + " - " + t.edificio + " de " + t.dono
            if t.estrada != "":
                linha = linha + " - estrada de " + t.estrada
            print(linha)
            if t.id % 4 == 0:
                print("----------")

    def mostrar_estado(self, jogadores, iniciado, terminado, atual):
        if len(jogadores) == 0:
            print("Não há jogadores.")
            return
        if terminado:
            print("O jogo terminou.")
        elif iniciado:
            print("Joga agora: " + jogadores[atual].nome)
        for j in jogadores:
            print(j.nome, "-", j.pontos, "pontos -", j.recursos)

    def mostrar_ajuda(self):
        print("Jogam 2 a 4 jogadores. Ganha quem chegar a 5 pontos.")
        print("Em cada turno lança os dados (LD). Aldeia dá 1 recurso e cidade dá 2. O 7 não dá nada.")
        print("Estrada: 1 madeira + 1 tijolo, ao lado de uma construção sua.")
        print("Aldeia: 1 madeira + 1 tijolo + 1 trigo, num terreno com estrada sua (1 ponto).")
        print("Cidade: 2 trigos + 2 minérios, em cima de uma aldeia sua (2 pontos).")
        print("Troca: 3 recursos iguais por 1 diferente.")
