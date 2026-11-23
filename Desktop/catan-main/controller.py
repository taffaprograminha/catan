from model import Jogo
from view import View


class Controller:

    def __init__(self):
        self.jogo = Jogo()
        self.view = View()

    def pedir_numero(self, texto):
        n = self.view.pedir(texto)
        if n.isdigit():
            return int(n)
        return 0

    def executar(self):
        print("UAL Catan - A Ilha das Possibilidades")
        while True:
            self.view.mostrar_menu()
            op = self.view.pedir("Escolha um comando: ").upper()

            if op == "RJ":
                self.registar_jogador()
            elif op == "IJ":
                self.iniciar_jogo()
            elif op == "LD":
                self.view.mostrar_mensagem(self.jogo.lancar_dados())
            elif op == "CE":
                n = self.pedir_numero("Número do terreno para a estrada: ")
                self.view.mostrar_mensagem(self.jogo.construir_estrada(n))
            elif op == "CA":
                n = self.pedir_numero("Número do terreno para a aldeia: ")
                self.view.mostrar_mensagem(self.jogo.construir_aldeia(n))
            elif op == "CC":
                n = self.pedir_numero("Número da aldeia a melhorar: ")
                self.view.mostrar_mensagem(self.jogo.construir_cidade(n))
            elif op == "TR":
                self.trocar_recursos()
            elif op == "FT":
                self.view.mostrar_mensagem(self.jogo.finalizar_turno())
            elif op == "G":
                nome = self.view.pedir("Nome do ficheiro JSON para gravar: ")
                self.view.mostrar_mensagem(self.jogo.gravar(nome))
            elif op == "L":
                nome = self.view.pedir("Nome do ficheiro JSON para carregar: ")
                self.view.mostrar_mensagem(self.jogo.ler(nome))
            elif op == "VT":
                self.view.mostrar_tabuleiro(self.jogo.terrenos)
            elif op == "EE":
                self.view.mostrar_estado(self.jogo.jogadores, self.jogo.iniciado, self.jogo.terminado, self.jogo.atual)
            elif op == "AJ":
                self.view.mostrar_ajuda()
            elif op == "S":
                print("Adeus!")
                break
            else:
                self.view.mostrar_mensagem("Comando inválido.")

    def registar_jogador(self):
        nome = self.view.pedir("Introduza o nome do jogador: ").strip()
        self.view.mostrar_mensagem(self.jogo.registar(nome))

    def iniciar_jogo(self):
        erro = self.jogo.pode_iniciar()
        if erro != "":
            self.view.mostrar_mensagem(erro)
            return
        escolhas = []
        for j in self.jogo.jogadores:
            escolhas.append(self.pedir_numero("Terreno inicial de " + j.nome + " (1-12): "))
        self.view.mostrar_mensagem(self.jogo.iniciar(escolhas))

    def trocar_recursos(self):
        dar = self.view.pedir("Recurso a entregar: ").lower()
        receber = self.view.pedir("Recurso a receber: ").lower()
        self.view.mostrar_mensagem(self.jogo.trocar(dar, receber))
