from PPlay.sprite import Sprite
from PPlay.window import Window
import config
import input

PES = 69


class Luffy:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 92
        self.height = 92
        self.vx = 0
        self.vy = 0
        self.chao = False
        self.direcao = 1
        self.estado = "parado"
        self.socando = False
        self.tempo_soco = 0
        self.tomando_dano = False
        self.tempo_dano = 0
        self.invencivel = 0
        self.vidas = 3
        self.plataforma = None
        self.fase_pulo = None
        self.tempo_fase_pulo = 0

        self.sprites = {}
        self.carregar()
        self.atual = self.sprites["parado_dir"]

    # carrega todos os sprites do Luffy
    def carregar(self):
        def fazer(nome, frames, dur):
            sp = Sprite(config.caminho(nome), frames)
            sp.set_total_duration(dur)
            return sp
        self.sprites["parado_dir"] = fazer("luffy_parado.png", 8, 900)
        self.sprites["parado_esq"] = fazer("luffy_parado_esq.png", 8, 900)
        self.sprites["andando_dir"] = fazer("luffy_andando.png", 6, 500)
        self.sprites["andando_esq"] = fazer("luffy_andando_esq.png", 6, 500)
        self.sprites["pulando_dir"] = fazer("luffy_pulando.png", 9, 700)
        self.sprites["pulando_esq"] = fazer("luffy_pulando_esq.png", 9, 700)
        self.sprites["agachado_dir"] = fazer("luffy_agachado.png", 5, 250)
        self.sprites["agachado_esq"] = fazer("luffy_agachado_esq.png", 5, 250)
        self.sprites["soco_dir"] = fazer("luffy_soco.png", 15, 420)
        self.sprites["soco_esq"] = fazer("luffy_soco_esq.png", 15, 420)
        self.sprites["machucado_dir"] = fazer("luffy_machucado.png", 6, 400)
        self.sprites["machucado_esq"] = fazer("luffy_machucado_esq.png", 6, 400)

        self.sprites["agachado_dir"].set_loop(False)
        self.sprites["agachado_esq"].set_loop(False)
        self.sprites["machucado_dir"].set_loop(False)
        self.sprites["machucado_esq"].set_loop(False)

    # atualiza a física e o input do jogador a cada frame
    def atualizar(self, plataformas):
        janela = Window.get_instance()
        dt = janela.delta_time()

        if not self.socando:
            mov = 0
            if input.esquerda():
                mov = mov - 1
                self.direcao = -1
            if input.direita():
                mov = mov + 1
                self.direcao = 1
            if input.agachar() and self.chao:
                mov = 0
            self.vx = mov * config.VEL_ANDAR
        else:
            self.vx = 0

        self.x = self.x + self.vx * dt

        if input.pulou() and self.chao and not self.socando and not input.agachar():
            self.vy = -config.FORCA_PULO
            self.chao = False

        if input.socou() and not self.socando and self.chao:
            self.socando = True
            self.tempo_soco = 0.42
            self.sprites["soco_dir"].set_curr_frame(0)
            self.sprites["soco_esq"].set_curr_frame(0)
            self.sprites["soco_dir"].play()
            self.sprites["soco_esq"].play()

        if self.socando:
            self.tempo_soco = self.tempo_soco - dt
            if self.tempo_soco <= 0:
                self.socando = False

        if self.tomando_dano:
            self.tempo_dano = self.tempo_dano - dt
            if self.tempo_dano <= 0:
                self.tomando_dano = False

        if not input.agachar():
            self.sprites["agachado_dir"].set_curr_frame(0)
            self.sprites["agachado_esq"].set_curr_frame(0)
            self.sprites["agachado_dir"].play()
            self.sprites["agachado_esq"].play()

        feet_antes = self.y + PES
        self.vy = self.vy + config.GRAVIDADE * dt
        self.y = self.y + self.vy * dt
        feet_depois = self.y + PES

        self.chao = False
        if self.vy >= 0:
            for p in plataformas:
                if self.x + 58 > p.x and self.x + 34 < p.x + p.width:
                    if feet_antes <= p.y + 4 and feet_depois >= p.y:
                        self.y = p.y - PES
                        self.vy = 0
                        self.chao = True
                        self.plataforma = p

        if self.invencivel > 0:
            self.invencivel = self.invencivel - dt

        if not self.chao:
            fase = "subindo" if self.vy < 0 else "descendo"
            if fase != self.fase_pulo:
                self.fase_pulo = fase
                self.tempo_fase_pulo = 0
            else:
                self.tempo_fase_pulo = self.tempo_fase_pulo + dt
        else:
            self.fase_pulo = None
            self.tempo_fase_pulo = 0

        self.definir_estado()

    # escolhe a animação certa para o estado atual do jogador
    def definir_estado(self):
        if self.direcao == 1:
            d = "dir"
        else:
            d = "esq"

        if self.tomando_dano:
            self.estado = "machucado"
        elif self.socando:
            self.estado = "soco"
        elif not self.chao:
            self.estado = "pulando"
        elif input.agachar():
            self.estado = "agachado"
        elif abs(self.vx) > 1:
            self.estado = "andando"
        else:
            self.estado = "parado"

        self.atual = self.sprites[self.estado + "_" + d]

        if self.estado == "pulando":
            
            if self.fase_pulo == "subindo":
                idx = min(4, int(self.tempo_fase_pulo / 0.05))
            else:
                idx = 4 + min(4, int(self.tempo_fase_pulo / 0.06))
            self.atual.set_curr_frame(idx)
        elif self.estado in ("parado", "andando", "soco", "agachado", "machucado"):
            self.atual.update()

    # desenha o Luffy na tela
    def desenhar(self):
        if self.invencivel > 0 and int(self.invencivel * 20) % 2 == 0:
            return
        sp = self.atual
        sp.x = self.x
        sp.y = self.y
        if self.estado == "agachado":
            sp.y = self.y + 7
        sp.draw()

    # retorna o hitbox do jogador
    def caixa(self):
        if self.estado == "agachado":
            return (self.x + 34, self.y + 40, 24, 29)
        return (self.x + 34, self.y + 22, 24, 47)

    # retorna o hitbox do soco se estiver ativo
    def caixa_soco(self):
        if not (self.socando and 0.056 < self.tempo_soco < 0.196):
            return None
        if self.direcao == 1:
            return (self.x + 48, self.y + 28, 18, 18)
        return (self.x + 26, self.y + 28, 18, 18)

    # aplica dano ao jogador e ativa a invencibilidade temporária
    def levar_dano(self):
        if self.invencivel > 0:
            return False
        self.vidas = self.vidas - 1
        self.invencivel = 1.2
        self.tomando_dano = True
        self.tempo_dano = 0.4
        self.sprites["machucado_dir"].set_curr_frame(0)
        self.sprites["machucado_esq"].set_curr_frame(0)
        self.sprites["machucado_dir"].play()
        self.sprites["machucado_esq"].play()
        return True

    # verifica se o jogador caiu na água
    def caiu(self):
        return self.y > config.ALTURA + 30

    # reposiciona o jogador na última plataforma que pisou
    def respawnar(self):
        p = self.plataforma
        self.x = p.x + p.width / 2 - 46
        self.y = p.y - PES
        self.vx = 0
        self.vy = 0
        self.chao = True
        self.invencivel = 1.0
