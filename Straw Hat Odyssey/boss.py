import random
from PPlay.sprite import Sprite
from PPlay.window import Window
import config

ESCALA_X_ESPINHO = 0.85
VELOCIDADE_ESPINHO = 850
NIVEIS_H = {
    "h_baixo": {"topo": -24, "altura": 30},
    "h_meio": {"topo": -45, "altura": 14},
    "h_alto": {"topo": -140, "altura": 50},
}


class Tentaculo:

    def __init__(self, x, y):
        self.sprite = Sprite(config.caminho("tentaculo_v.png"), 2)
        self.sprite.set_total_duration(400)
        self.vida_ativa = 1.0
        self.sprite.x = x
        self.sprite.y = y
        self.atraso = config.preview_tempo[config.dificuldade]
        self.morto = False

    # atualiza o tempo de vida do tentáculo
    def atualizar(self):
        dt = Window.get_instance().delta_time()
        if self.atraso > 0:
            self.atraso = self.atraso - dt
        else:
            self.vida_ativa = self.vida_ativa - dt
            if self.vida_ativa <= 0:
                self.morto = True
        self.sprite.update()

    # verifica se o tentáculo já pode causar dano
    def perigoso(self):
        return self.atraso <= 0

    # retorna o hitbox do tentáculo
    def caixa(self):
        s = self.sprite
        return (s.x + 18, s.y + 10, s.width - 36, s.height - 14)

    # desenha o tentáculo na tela
    def desenhar(self):
        if self.atraso > 0:
            self.sprite.set_transparency(85)
        else:
            self.sprite.set_transparency(255)
        self.sprite.draw()
        self.sprite.set_transparency(255)


class Espinho:

    def __init__(self, nivel, x_kraken, deck_x, deck_y):
        info = NIVEIS_H[nivel]
        self.hit_topo = info["topo"]
        self.hit_altura = info["altura"]
        self.deck_x = deck_x
        self.deck_y = deck_y

        self.sprite = Sprite(config.caminho("tentaculo_h_lancado.png"), 2)
        self.sprite.set_total_duration(300)
        self.escala_x = ESCALA_X_ESPINHO
        self.escala_y = (self.hit_altura + 20) / self.sprite.height
        self.sprite.set_scale(self.escala_x, self.escala_y)
        self.largura = self.sprite.width * self.escala_x

        self.x = x_kraken - self.largura
        self.sprite.x = self.x
        self.sprite.y = deck_y + self.hit_topo - 10

        self.atraso = config.preview_tempo[config.dificuldade]
        self.lancado = False
        self.morto = False

    # atualiza a posição do espinho
    def atualizar(self):
        dt = Window.get_instance().delta_time()
        if self.atraso > 0:
            self.atraso = self.atraso - dt
        else:
            self.lancado = True
            self.x = self.x - VELOCIDADE_ESPINHO * dt
            self.sprite.x = self.x
            if self.x + self.largura < self.deck_x:
                self.morto = True
        self.sprite.update()

    # verifica se o espinho está em movimento
    def perigoso(self):
        return self.lancado

    # retorna o hitbox do espinho
    def caixa(self):
        if not self.perigoso():
            return None
        return (self.x + 10, self.deck_y + self.hit_topo, self.largura - 20, self.hit_altura)

    # desenha o espinho na tela
    def desenhar(self):
        if self.atraso > 0:
            self.sprite.set_transparency(80)
        else:
            self.sprite.set_transparency(255)
        self.sprite.draw()
        self.sprite.set_transparency(255)


class Kraken:
    def __init__(self, x, y):
        self.sprite = Sprite(config.caminho("kraken.png"), 3)
        self.sprite.set_total_duration(800)
        self.sprite.x = x
        self.sprite.y = y
        self.hp = 8
        self.invuln = 0
        self.flash = 0
        self.tempo = 2.0
        self.tentaculos = []
        self.ativo = False

    # retorna o hitbox do kraken
    def caixa(self):
        s = self.sprite
        return (s.x + 30, s.y + 20, 80, 70)

    # atualiza o kraken e seus tentáculos
    def atualizar(self, player, deck_x, deck_y, deck_w):
        dt = Window.get_instance().delta_time()
        self.sprite.update()

        if self.invuln > 0:
            self.invuln = self.invuln - dt
        if self.flash > 0:
            self.flash = self.flash - dt

        if self.ativo and self.hp > 0:
            self.tempo = self.tempo - dt
            if self.tempo <= 0:
                self.atacar(player, deck_x, deck_y, deck_w)
                self.tempo = config.cooldown_boss[config.dificuldade]

        vivos = []
        for t in self.tentaculos:
            t.atualizar()
            if not t.morto:
                vivos.append(t)
        self.tentaculos = vivos

    # escolhe e lança um ataque aleatório
    def atacar(self, player, deck_x, deck_y, deck_w):
        tipo = random.choice(["h_baixo", "h_meio", "h_alto", "v", "v"])
        if tipo == "v":
            quantos = random.choice([1, 2])
            for _ in range(quantos):
                tx = random.randint(int(player.x - 300), int(player.x + 300))
                if tx < deck_x + 40:
                    tx = deck_x + 40
                if tx > deck_x + deck_w - 120:
                    tx = deck_x + deck_w - 120
                self.tentaculos.append(Tentaculo(tx, config.ALTURA - 298))
        else:
            x_kraken = self.sprite.x + self.sprite.width
            self.tentaculos.append(Espinho(tipo, x_kraken, deck_x, deck_y))

    # aplica dano ao kraken
    def levar_soco(self):
        if self.invuln > 0:
            return False
        self.hp = self.hp - 1
        self.invuln = 0.5
        self.flash = 0.2
        return True

    # desenha o kraken e seus tentáculos na tela
    def desenhar(self):
        if self.flash > 0 and int(self.flash * 30) % 2 == 0:
            self.sprite.set_transparency(140)
        else:
            self.sprite.set_transparency(255)
        self.sprite.draw()
        self.sprite.set_transparency(255)
        for t in self.tentaculos:
            t.desenhar()
