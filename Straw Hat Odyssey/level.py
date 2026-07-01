import pygame
from PPlay.sprite import Sprite
from PPlay.gameimage import GameImage
import config


class Plataforma:
    # carrega a imagem da plataforma
    def __init__(self, nome, x, y, escala=1.0):
        self.sprite = Sprite(config.caminho(nome), 1)
        if escala != 1.0:
            self.sprite.set_scale(escala)
        self.sprite.x = x
        self.sprite.y = y
        self.x = x
        self.y = y
        self.width = self.sprite.width * escala

    # desenha a plataforma na tela
    def desenhar(self):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.draw()


class Cenario:
    # monta todo o cenário do jogo
    def __init__(self):
        self.fundo = GameImage(config.caminho("fundo.png"))
        self.fundo.image = pygame.transform.scale(
            self.fundo.image, (config.LARGURA, config.ALTURA)
        )
        self.fundo.width = config.LARGURA
        self.fundo.height = config.ALTURA
        self.plataformas = []

        dados = [
            ("navio_merry.png", 40, 400, 1.0),
            ("barco1.png", 520, 400, 1.0),
            ("barco2.png", 1120, 370, 1.0),
            ("barco3.png", 1720, 405, 1.0),
            ("barco4.png", 2320, 375, 1.0),
            ("barco5.png", 2920, 405, 1.0),
            # navio do boss escalado para caber na arena
            ("navio_boss.png", 3560, 395, (0.8 * config.LARGURA) / 1500),
        ]
        for nome, x, y, escala in dados:
            self.plataformas.append(Plataforma(nome, x, y, escala))

        self.inicio = self.plataformas[0]
        self.barcos = self.plataformas[1:6]
        self.navio_boss = self.plataformas[6]

        # plataformas extras em cima de alguns barcos
        extras = [
            (self.barcos[0], "caixote.png", 44, 380),
            (self.barcos[1], "mastro.png", 88, 50),
            (self.barcos[3], "caixote.png", 44, 60),
            (self.barcos[4], "mastro.png", 88, 270),
        ]
        self.extras = []
        for barco, nome, altura, offset_x in extras:
            extra = Plataforma(nome, barco.x + offset_x, barco.y - altura)
            self.plataformas.append(extra)
            self.extras.append(extra)
        self.largura_mundo = self.navio_boss.x + self.navio_boss.width

    # desenha o fundo e todas as plataformas
    def desenhar(self):
        self.fundo.x = 0
        self.fundo.y = 0
        self.fundo.draw()
        for p in self.plataformas:
            p.desenhar()
