import pygame
from PPlay.window import Window
from PPlay.gameimage import GameImage
import config
import input
import ranking


class Menu:
    def __init__(self):
        self.janela = Window.get_instance()
        self.fundo = GameImage(config.caminho("menu_fundo.png"))
        self.fundo.image = pygame.transform.scale(
            self.fundo.image, (config.LARGURA, config.ALTURA)
        )
        self.fundo.width = config.LARGURA
        self.fundo.height = config.ALTURA
        
        self.tabua = GameImage(config.caminho("tabua.png"))
        self.logo = GameImage(config.caminho("menu_logo.png"))
        self.tela = "principal"
        self.nome = ""
        self.resultado = ""
        self.tempo = 0
        self.lista_ranking = []

        # carrega a fonte personalizada do jogo
        self.fonte = pygame.font.Font(config.FONTE, 26)

    # prepara a tela de digitar o nome após o fim da partida
    def iniciar_nome(self, resultado, tempo):
        self.tela = "nome"
        self.resultado = resultado
        self.tempo = tempo
        self.nome = ""

    # desenha texto centralizado na tela
    def texto_centro(self, texto, cx, y, tam, cor):
        f = pygame.font.Font(config.FONTE, tam)
        surf = f.render(str(texto), True, cor)
        w = surf.get_width()
        Window.get_screen().blit(surf, (cx - w / 2, y))

    # desenha um botão de tábua de madeira e retorna seu rect
    def botao(self, texto, y, x=70):
        self.tabua.x = x
        self.tabua.y = y
        self.tabua.draw()
        self.texto_centro(texto, x + 120, y + 18, 26, (70, 35, 12))
        return (x, y, 240, 68)

    # verifica se o jogador clicou dentro de um botão
    def clicou_em(self, rect):
        if not input.clicou():
            return False
        mx, my = input.pos_mouse()
        x, y, w, h = rect
        return x <= mx <= x + w and y <= my <= y + h

    # desenha a imagem de fundo do menu
    def desenhar_fundo(self):
        self.fundo.x = 0
        self.fundo.y = 0
        self.fundo.draw()

    # decide qual tela do menu atualizar
    def atualizar(self):
        self.desenhar_fundo()
        if self.tela == "principal":
            return self.tela_principal()
        if self.tela == "dificuldade":
            return self.tela_dificuldade()
        if self.tela == "ranking":
            return self.tela_ranking()
        if self.tela == "nome":
            return self.tela_nome()
        return None

    # mostra o menu principal com os botões de jogar, dificuldade, ranking e sair
    def tela_principal(self):
        logo_escala = min(config.LARGURA * 0.85 / self.logo.width, 240 / self.logo.height)
        logo_w = self.logo.width * logo_escala
        logo_h = self.logo.height * logo_escala
        self.logo.set_scale(logo_escala)
        self.logo.x = config.LARGURA / 2 - logo_w / 2
        self.logo.y = 10
        self.logo.draw()

        base_y = 10 + logo_h + 10
        espacamento = 64
        
        b1 = self.botao("Jogar", base_y)
        b2 = self.botao("Dificuldade", base_y + espacamento)
        b3 = self.botao("Ranking", base_y + espacamento * 2)
        b4 = self.botao("Sair", base_y + espacamento * 3)
        
        if self.clicou_em(b1):
            return "jogar"
        if self.clicou_em(b2):
            self.tela = "dificuldade"
        if self.clicou_em(b3):
            self.lista_ranking = ranking.carregar()
            self.tela = "ranking"
        if self.clicou_em(b4):
            return "sair"
        return None

    # mostra as opções de dificuldade
    def tela_dificuldade(self):
        self.texto_centro("DIFICULDADE", config.LARGURA / 2, 44, 40, (255, 240, 180))
        self.texto_centro("Atual: " + config.dificuldade, config.LARGURA / 2, 92, 24, (240, 240, 248))
        b1 = self.botao("Facil", 190)
        b2 = self.botao("Medio", 268)
        b3 = self.botao("Dificil", 346)
        b4 = self.botao("Voltar", 424)
        if self.clicou_em(b1):
            config.dificuldade = "Facil"
        if self.clicou_em(b2):
            config.dificuldade = "Medio"
        if self.clicou_em(b3):
            config.dificuldade = "Dificil"
        if self.clicou_em(b4) or input.voltar():
            self.tela = "principal"
        return None

    # mostra o ranking dos melhores jogadores
    def tela_ranking(self):
        self.texto_centro("RANKING", config.LARGURA / 2, 36, 40, (255, 240, 180))
        self.texto_centro("Vitorias pelo menor tempo. Derrotas por ordem de chegada.",
                          config.LARGURA / 2, 82, 18, (235, 235, 245))
        if len(self.lista_ranking) == 0:
            self.texto_centro("Ainda nao ha registros", config.LARGURA / 2, 200, 24, (255, 255, 255))
        else:
            y = 120
            pos = 1
            for item in self.lista_ranking[:9]:
                nome = item[0]
                tempo = item[1]
                res = item[2]
                if res == "venceu":
                    marca = "Vitoria"
                else:
                    marca = "Derrota"
                linha = str(pos) + ".  " + nome + "  -  " + str(tempo) + "s  (" + marca + ")"
                self.texto_centro(linha, config.LARGURA / 2, y, 24, (255, 255, 255))
                y = y + 32
                pos = pos + 1
        b = self.botao("Voltar", 470, config.LARGURA / 2 - 120)
        if self.clicou_em(b) or input.voltar():
            self.tela = "principal"
        return None

    # tela para o jogador digitar o nome após a partida
    def tela_nome(self):
        if self.resultado == "venceu":
            self.texto_centro("VOCE VENCEU!", config.LARGURA / 2, 70, 46, (185, 255, 185))
        else:
            self.texto_centro("VOCE PERDEU", config.LARGURA / 2, 70, 46, (255, 180, 180))
        self.texto_centro("Tempo: " + str(round(self.tempo, 1)) + "s", config.LARGURA / 2, 138, 26, (255, 255, 255))
        self.texto_centro("Digite seu nome e aperte ENTER:", config.LARGURA / 2, 210, 24, (240, 240, 248))
        self.botao("", 250, config.LARGURA / 2 - 120)
        self.texto_centro(self.nome + "_", config.LARGURA / 2, 268, 26, (70, 35, 12))
        self.nome, pronto = input.digitar(self.nome)
        if pronto:
            ranking.salvar(self.nome, self.tempo, self.resultado)
            self.lista_ranking = ranking.carregar()
            self.tela = "ranking"
        return None
