import pygame
from PPlay.window import Window
from PPlay.camera import Camera
from PPlay.gameimage import GameImage
from PPlay.effects import ScreenEffects
import config
import input
import musica
from level import Cenario
from player import Luffy, PES
from enemies import criar_inimigos
from boss import Kraken


# verifica se dois retângulos se sobrepõem
def bater(a, b):
    if a is None or b is None:
        return False
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


class Jogo:
    def __init__(self):
        self.janela = Window.get_instance()
        self.cenario = Cenario()
        self.camera = Camera(config.LARGURA, config.ALTURA)
        self.camera.set_world_bounds(self.cenario.largura_mundo, config.ALTURA)

        self.player = Luffy()
        self.player.plataforma = self.cenario.inicio
        self.player.x = self.cenario.inicio.x + 60
        self.player.y = self.cenario.inicio.y - PES

        self.inimigos = criar_inimigos(self.cenario.barcos)

        navio = self.cenario.navio_boss
        self.kraken = Kraken(navio.x + navio.width - 130, navio.y - 110)

        self.coracao = GameImage(config.caminho("coracao.png"))
        self.coracao_vazio = GameImage(config.caminho("coracao_vazio.png"))

        # carrega a imagem do botão de pausa
        self.tabua = GameImage(config.caminho("tabua.png"))

        self.tempo = 0
        self.terminou = False
        self.resultado = ""
        self.pausado = False
        self.boss_musica_ativa = False

    # atualiza a lógica do jogo a cada frame
    def atualizar(self):
        if input.voltar():
            self.pausado = not self.pausado

        if self.pausado:
            # verifica clique nos botões de pausa
            rect_voltar = self._rect_botao_pausa(200)
            rect_menu = self._rect_botao_pausa(280)

            if input.clicou():
                mx, my = input.pos_mouse()
                if self._dentro(mx, my, rect_voltar):
                    self.pausado = False
                elif self._dentro(mx, my, rect_menu):
                    self.pausado = False
                    return "menu"
            return None

        dt = self.janela.delta_time()
        self.tempo = self.tempo + dt

        plataformas = self.cenario.plataformas
        self.player.atualizar(plataformas)

        if self.player.caiu():
            self.player.vidas = self.player.vidas - 1
            ScreenEffects.shake(8, 0.3)
            self.player.respawnar()
            if self.player.vidas <= 0:
                self.finalizar("perdeu")
                return None

        navio = self.cenario.navio_boss
        if self.player.x > navio.x + 40:
            self.kraken.ativo = True
            if not self.boss_musica_ativa:
                musica.tocar_boss()
                self.boss_musica_ativa = True

        for ini in self.inimigos:
            ini.atualizar(self.player)

        soco = self.player.caixa_soco()
        for ini in self.inimigos:
            if not ini.morto and bater(soco, ini.caixa()):
                ini.levar_soco()
        vivos = []
        for ini in self.inimigos:
            if not ini.morto:
                vivos.append(ini)
        self.inimigos = vivos

        for ini in self.inimigos:
            if bater(ini.espada(), self.player.caixa()):
                if self.player.levar_dano():
                    ScreenEffects.shake(6, 0.25)

        self.kraken.atualizar(self.player, navio.x, navio.y, navio.width)

        if self.kraken.ativo and bater(soco, self.kraken.caixa()):
            if self.kraken.levar_soco():
                ScreenEffects.shake(7, 0.3)

        for t in self.kraken.tentaculos:
            if t.perigoso() and bater(t.caixa(), self.player.caixa()):
                if self.player.levar_dano():
                    ScreenEffects.shake(7, 0.3)

        if self.player.vidas <= 0:
            self.finalizar("perdeu")
            return None
        if self.kraken.hp <= 0:
            self.finalizar("venceu")
            return None

        if self.kraken.ativo:
            # trava a câmera na arena do boss
            alvo_x = self.camera.limite_direita
            alvo_y = self.camera.limite_topo
            self.camera.x += (alvo_x - self.camera.x) * 0.05
            self.camera.y += (alvo_y - self.camera.y) * 0.05
        else:
            self.camera.follow(self.player, 0.12)
        ScreenEffects.update()
        ScreenEffects.apply_to_camera()
        return None

    # retorna o rect de um botão de pausa centralizado
    def _rect_botao_pausa(self, y):
        x = config.LARGURA / 2 - 120
        return (x, y, 240, 68)

    # verifica se o mouse está dentro de um retângulo
    def _dentro(self, mx, my, rect):
        x, y, w, h = rect
        return x <= mx <= x + w and y <= my <= y + h

    # marca o fim do jogo com o resultado
    def finalizar(self, resultado):
        self.resultado = resultado
        self.terminou = True

    # desenha todos os elementos do jogo na tela
    def desenhar(self):
        self.cenario.desenhar()
        for ini in self.inimigos:
            ini.desenhar()
        self.kraken.desenhar()
        self.player.desenhar()
        ScreenEffects.draw_flash()
        self.desenhar_hud()

        if self.pausado:
            self.desenhar_pausa()

    # desenha a tela de pausa sobre o jogo
    def desenhar_pausa(self):
        tela = Window.get_screen()

        overlay = pygame.Surface((config.LARGURA, config.ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        tela.blit(overlay, (0, 0))

        f_titulo = pygame.font.Font(config.FONTE, 42)
        titulo_surf = f_titulo.render("PAUSADO", True, (255, 240, 180))
        titulo_w = titulo_surf.get_width()
        tela.blit(titulo_surf, (config.LARGURA / 2 - titulo_w / 2, 110))

        self._desenhar_botao_pausa("Voltar ao Jogo", 200)
        self._desenhar_botao_pausa("Menu", 280)

    # desenha um botão de tábua de madeira na tela de pausa
    def _desenhar_botao_pausa(self, texto, y):
        tela = Window.get_screen()
        x = config.LARGURA / 2 - 120
        self.tabua.x = x
        self.tabua.y = y
        self.tabua.draw()
        f = pygame.font.Font(config.FONTE, 24)
        txt_surf = f.render(texto, True, (70, 35, 12))
        txt_w = txt_surf.get_width()
        tela.blit(txt_surf, (x + 120 - txt_w / 2, y + 18))

    # desenha a vida e o tempo na tela
    def desenhar_hud(self):
        for i in range(3):
            if i < self.player.vidas:
                img = self.coracao
            else:
                img = self.coracao_vazio
            img.x = 12 + i * 38
            img.y = 12
            img.draw()
        self.janela.draw_text("Tempo: " + str(round(self.tempo, 1)), 12, 56, tamanho=22, cor=(255, 255, 255))
        if self.kraken.ativo and self.kraken.hp > 0:
            self.desenhar_vida_boss()

    # desenha a barra de vida do boss
    def desenhar_vida_boss(self):
        tela = Window.get_screen()
        largura = 300
        x = config.LARGURA / 2 - largura / 2
        y = 24
        pygame.draw.rect(tela, (60, 30, 30), (x - 2, y - 2, largura + 4, 18))
        proporcao = self.kraken.hp / 8.0
        pygame.draw.rect(tela, (210, 60, 60), (x, y, largura * proporcao, 14))
        self.janela.draw_text("KRAKEN", x + largura / 2 - 32, y - 24, tamanho=20, cor=(255, 220, 220))
