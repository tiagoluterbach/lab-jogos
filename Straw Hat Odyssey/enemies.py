from PPlay.sprite import Sprite
from PPlay.window import Window
import config

PES = 69


class Marinheiro:
    def __init__(self, plataforma):
        self.plat = plataforma
        self.x = plataforma.x + plataforma.width / 2 - 40
        self.y = plataforma.y - PES
        self.vx = 45
        self.direcao = -1
        self.hp = 2
        self.invuln = 0
        self.estado = "andando"
        self.atacando = False
        self.tempo_ataque = 0
        self.cooldown = 1.0
        self.tomando_dano = False
        self.tempo_dano = 0
        self.morrendo = False
        self.tempo_morrendo = 0
        self.morto = False

        self.sprites = {}
        self.carregar()
        self.atual = self.sprites["andando_esq"]

    # carrega todos os sprites do marinheiro
    def carregar(self):
        def fazer(nome, frames, dur, loop=True):
            sp = Sprite(config.caminho(nome), frames)
            sp.set_total_duration(dur)
            sp.set_loop(loop)
            return sp
        self.sprites["parado_dir"] = fazer("marinheiro_parado.png", 4, 700)
        self.sprites["parado_esq"] = fazer("marinheiro_parado_esq.png", 4, 700)
        self.sprites["andando_dir"] = fazer("marinheiro_andando.png", 6, 550)
        self.sprites["andando_esq"] = fazer("marinheiro_andando_esq.png", 6, 550)
        self.sprites["atacando_dir"] = fazer("marinheiro_atacando.png", 9, 500)
        self.sprites["atacando_esq"] = fazer("marinheiro_atacando_esq.png", 9, 500)
        self.sprites["machucado_dir"] = fazer("marinheiro_machucado.png", 6, 350, loop=False)
        self.sprites["machucado_esq"] = fazer("marinheiro_machucado_esq.png", 6, 350, loop=False)
        self.sprites["morrendo_dir"] = fazer("marinheiro_morrendo.png", 7, 550, loop=False)
        self.sprites["morrendo_esq"] = fazer("marinheiro_morrendo_esq.png", 7, 550, loop=False)

    # atualiza o comportamento do inimigo a cada frame
    def atualizar(self, player):
        dt = Window.get_instance().delta_time()

        if self.morrendo:
            self.tempo_morrendo = self.tempo_morrendo - dt
            if self.tempo_morrendo <= 0:
                self.morto = True
            d = "dir" if self.direcao == 1 else "esq"
            self.atual = self.sprites["morrendo_" + d]
            self.atual.update()
            return

        if self.invuln > 0:
            self.invuln = self.invuln - dt
        if self.tomando_dano:
            self.tempo_dano = self.tempo_dano - dt
            if self.tempo_dano <= 0:
                self.tomando_dano = False

        if player.x < self.x:
            self.direcao = -1
        else:
            self.direcao = 1

        dist = abs((player.x + 32) - (self.x + 40))
        mesma_altura = abs(player.y - self.y) < 70

        movendo = False
        if self.atacando:
            self.tempo_ataque = self.tempo_ataque - dt
            if self.tempo_ataque <= 0:
                self.atacando = False
                self.cooldown = config.cooldown_inimigo[config.dificuldade]
        elif self.tomando_dano:
            pass
        else:
            if self.cooldown > 0:
                self.cooldown = self.cooldown - dt
            if dist < 120 and mesma_altura and self.cooldown <= 0:
                self.atacando = True
                self.tempo_ataque = 0.55
                self.sprites["atacando_dir"].set_curr_frame(0)
                self.sprites["atacando_esq"].set_curr_frame(0)
                self.sprites["atacando_dir"].play()
                self.sprites["atacando_esq"].play()
            elif dist > 170:
                movendo = True
                self.x = self.x + self.vx * dt
                if self.x < self.plat.x + 6:
                    self.x = self.plat.x + 6
                    self.vx = abs(self.vx)
                if self.x > self.plat.x + self.plat.width - 86:
                    self.x = self.plat.x + self.plat.width - 86
                    self.vx = -abs(self.vx)
                if self.vx < 0:
                    self.direcao = -1
                else:
                    self.direcao = 1
        
        if self.direcao == 1:
            d = "dir"
        else:
            d = "esq"
        if self.tomando_dano:
            self.estado = "machucado"
        elif self.atacando:
            self.estado = "atacando"
        elif movendo:
            self.estado = "andando"
        else:
            self.estado = "parado"
        self.atual = self.sprites[self.estado + "_" + d]
        self.atual.update()

    # retorna o hitbox do inimigo
    def caixa(self):
        if self.morrendo:
            return None
        return (self.x + 14, self.y + 8, 28, 54)

    # retorna o hitbox da espada se estiver atacando
    def espada(self):
        if self.morrendo:
            return None
        if not (self.atacando and 0.183 < self.tempo_ataque < 0.367):
            return None
        if self.direcao == 1:
            return (self.x + 45, self.y + 18, 25, 14)
        return (self.x + 22, self.y + 18, 25, 14)

    # aplica dano ao inimigo
    def levar_soco(self):
        if self.invuln > 0 or self.morrendo:
            return
        self.hp = self.hp - 1
        self.invuln = 0.45
        self.tomando_dano = True
        self.tempo_dano = 0.3
        self.sprites["machucado_dir"].set_curr_frame(0)
        self.sprites["machucado_esq"].set_curr_frame(0)
        self.sprites["machucado_dir"].play()
        self.sprites["machucado_esq"].play()
        if self.hp <= 0:
            self.morrendo = True
            self.tempo_morrendo = 0.55
            self.sprites["morrendo_dir"].set_curr_frame(0)
            self.sprites["morrendo_esq"].set_curr_frame(0)
            self.sprites["morrendo_dir"].play()
            self.sprites["morrendo_esq"].play()

    # desenha o inimigo na tela
    def desenhar(self):
        if self.invuln > 0 and not self.morrendo and int(self.invuln * 20) % 2 == 0:
            self.atual.set_transparency(120)
        else:
            self.atual.set_transparency(255)
        self.atual.x = self.x
        self.atual.y = self.y
        self.atual.draw()
        self.atual.set_transparency(255)


# cria um inimigo por barco e retorna a lista
def criar_inimigos(barcos):
    lista = []
    for i in range(len(barcos)):
        lista.append(Marinheiro(barcos[i]))
    return lista
