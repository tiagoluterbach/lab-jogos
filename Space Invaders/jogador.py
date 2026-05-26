from PPlay.sprite import Sprite
from PPlay.keyboard import Keyboard

class Jogador:
    def __init__(self, janela):
        self.janela = janela
        self.teclado = Keyboard()
        self.sprite = Sprite("player.png")
        self.sprite.set_position(self.janela.width / 2 - self.sprite.width / 2, self.janela.height - self.sprite.height + 200)
        self.velocidade = 300
        self.velocidade_tiro = 500
        self.tiros = []
        self.tempo_recarga = 0
        self.margem_borda = 30 

    def update(self, dificuldade):
        dt = self.janela.delta_time()
        
        if self.teclado.key_pressed("LEFT"):
            self.sprite.x -= self.velocidade * dt
        if self.teclado.key_pressed("RIGHT"):
            self.sprite.x += self.velocidade * dt

        if self.sprite.x < -self.margem_borda:
            self.sprite.x = -self.margem_borda
        elif self.sprite.x + self.sprite.width > self.janela.width + self.margem_borda:
            self.sprite.x = self.janela.width - self.sprite.width + self.margem_borda

        if dificuldade == 1:
            cooldown = 0.8
        elif dificuldade == 2:
            cooldown = 0.4
        else:
            cooldown = 0.2

        self.tempo_recarga -= dt

        if self.teclado.key_pressed("SPACE") and self.tempo_recarga <= 0:
            tiro = Sprite("tiro.png")
            tiro.set_position(self.sprite.x + self.sprite.width / 2 - tiro.width / 2, self.sprite.y)
            self.tiros.append(tiro)
            self.tempo_recarga = cooldown

        for tiro in self.tiros[:]:
            tiro.y -= self.velocidade_tiro * dt
            if tiro.y + tiro.height < 0:
                self.tiros.remove(tiro)

    def draw(self):
        self.sprite.draw()
        for tiro in self.tiros:
            tiro.draw()