from PPlay.window import Window
from PPlay.sprite import Sprite

LARGURA_JANELA = 800
ALTURA_JANELA = 600
janela = Window(LARGURA_JANELA, ALTURA_JANELA, "Pong - Tiago Luterbach")

teclado = janela.keyboard
VELOCIDADE_BOLA_BASE = 400
VELOCIDADE_BOLA_MAX = 900
VELOCIDADE_JOGADOR = 500
VELOCIDADE_IA_BASE = 350 
INCLINACOES_SERVE = [-0.7, -0.35, 0.35, 0.7]

bola = Sprite("bola.png") 
barra_esq_ia = Sprite("raquete.png") 
barra_dir_player = Sprite("raquete.png") 

direcao_serve_x = 1
indice_inclinacao_serve = 0

def resetar_bola():
    global direcao_serve_x, indice_inclinacao_serve

    bola.x = janela.largura / 2 - bola.width / 2
    bola.y = janela.altura / 2 - bola.height / 2

    inclinacao = INCLINACOES_SERVE[indice_inclinacao_serve]
    vel_x = VELOCIDADE_BOLA_BASE * direcao_serve_x
    vel_y = VELOCIDADE_BOLA_BASE * inclinacao

    direcao_serve_x *= -1
    indice_inclinacao_serve = (indice_inclinacao_serve + 1) % len(INCLINACOES_SERVE)

    return vel_x, vel_y

def centralizar_barras():
    barra_esq_ia.x = 10 
    barra_esq_ia.y = janela.altura / 2 - barra_esq_ia.height / 2
    
    barra_dir_player.x = janela.largura - barra_dir_player.width - 10
    barra_dir_player.y = janela.altura / 2 - barra_dir_player.height / 2

centralizar_barras()
vel_bola_x, vel_bola_y = 0, 0 
aguardando_serve = True 

# Placar
pontos_ia = 0
pontos_player = 0

#jogo
while True:
    
    janela.set_background_color((0, 0, 0))
    dt = janela.delta_time()
    
    if dt > 0.1:
        dt = 0.1

    if aguardando_serve:
        if teclado.key_pressed("SPACE"):
            vel_bola_x, vel_bola_y = resetar_bola()
            aguardando_serve = False
            
    else:
        
        if teclado.key_pressed("UP"):
            barra_dir_player.y -= VELOCIDADE_JOGADOR * dt
        if teclado.key_pressed("DOWN"):
            barra_dir_player.y += VELOCIDADE_JOGADOR * dt
            
        centro_ia = barra_esq_ia.y + barra_esq_ia.height / 2
        centro_bola = bola.y + bola.height / 2
        
        if centro_bola < centro_ia - 10: 
            barra_esq_ia.y -= VELOCIDADE_IA_BASE * dt
        elif centro_bola > centro_ia + 10:
            barra_esq_ia.y += VELOCIDADE_IA_BASE * dt

        x_anterior_bola = bola.x
        bola.x += vel_bola_x * dt
        bola.y += vel_bola_y * dt

        for barra in [barra_esq_ia, barra_dir_player]:
            if barra.y < 0:
                barra.y = 0
            if barra.y + barra.height > janela.altura:
                barra.y = janela.altura - barra.height

        if bola.y <= 0:
            bola.y = 0
            vel_bola_y *= -1
        elif bola.y + bola.height >= janela.altura:
            bola.y = janela.altura - bola.height 
            vel_bola_y *= -1

        colidiu_esq = (
            vel_bola_x < 0
            and bola.y < barra_esq_ia.y + barra_esq_ia.height
            and bola.y + bola.height > barra_esq_ia.y
            and x_anterior_bola >= barra_esq_ia.x + barra_esq_ia.width
            and bola.x <= barra_esq_ia.x + barra_esq_ia.width
        )
        colidiu_dir = (
            vel_bola_x > 0
            and bola.y < barra_dir_player.y + barra_dir_player.height
            and bola.y + bola.height > barra_dir_player.y
            and x_anterior_bola + bola.width <= barra_dir_player.x
            and bola.x + bola.width >= barra_dir_player.x
        )

        if not colidiu_esq and vel_bola_x < 0 and bola.collided(barra_esq_ia):
            colidiu_esq = True
        if not colidiu_dir and vel_bola_x > 0 and bola.collided(barra_dir_player):
            colidiu_dir = True

        if colidiu_esq:
            bola.x = barra_esq_ia.x + barra_esq_ia.width
            vel_bola_x = abs(vel_bola_x) * 1.05

            deslocamento = (bola.y + bola.height / 2) - (barra_esq_ia.y + barra_esq_ia.height / 2)
            vel_bola_y += deslocamento * 2.5

        elif colidiu_dir:
            bola.x = barra_dir_player.x - bola.width
            vel_bola_x = -abs(vel_bola_x) * 1.05

            deslocamento = (bola.y + bola.height / 2) - (barra_dir_player.y + barra_dir_player.height / 2)
            vel_bola_y += deslocamento * 2.5

        velocidade_total = (vel_bola_x ** 2 + vel_bola_y ** 2) ** 0.5
        if velocidade_total > VELOCIDADE_BOLA_MAX:
            fator = VELOCIDADE_BOLA_MAX / velocidade_total
            vel_bola_x *= fator
            vel_bola_y *= fator
        
        if bola.x + bola.width < 0:
            pontos_player += 1
            aguardando_serve = True
            vel_bola_x, vel_bola_y = 0, 0
            centralizar_barras() 

        elif bola.x > janela.largura:
            pontos_ia += 1
            aguardando_serve = True
            vel_bola_x, vel_bola_y = 0, 0
            centralizar_barras()
    
    if aguardando_serve:
        janela.draw_text("Pressione ESPAÇO", LARGURA_JANELA/2 - 130, ALTURA_JANELA/2 + 50, tamanho=30, cor=(0, 255, 0))

    bola.draw()
    barra_esq_ia.draw()
    barra_dir_player.draw()

    janela.draw_text("IA", LARGURA_JANELA / 2 - 110, 10, tamanho=24, cor=(180, 180, 180))
    janela.draw_text("JOGADOR", LARGURA_JANELA / 2 + 45, 10, tamanho=24, cor=(180, 180, 180))
    janela.draw_text(f"{pontos_ia} : {pontos_player}", LARGURA_JANELA / 2 - 45, 40, tamanho=40, cor=(255, 255, 255))

    janela.update()