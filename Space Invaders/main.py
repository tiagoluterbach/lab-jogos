from PPlay.window import Window
from PPlay.mouse import Mouse
from PPlay.sprite import Sprite
from PPlay.keyboard import Keyboard
from jogador import Jogador

LARGURA_JANELA = 800
ALTURA_JANELA = 600
janela = Window(LARGURA_JANELA, ALTURA_JANELA)
janela.set_title("Space Invaders")
mouse = Mouse() 
teclado = Keyboard()

btn_jogar = Sprite("btnjogar.png") 
btn_dificuldade = Sprite("btndificuldade.png")
btn_ranking = Sprite("btnranking.png")
btn_sair = Sprite("btnsair.png")

btn_facil = Sprite("btnfacil.png")
btn_medio = Sprite("btnmedio.png")
btn_dificil = Sprite("btndificil.png")

btn_jogar.set_position(janela.width/2 - btn_jogar.width/2, janela.height/2 - 225)
btn_dificuldade.set_position(janela.width/2 - btn_dificuldade.width/2, janela.height/2 - 75)
btn_ranking.set_position(janela.width/2 - btn_ranking.width/2, janela.height/2 + 75)
btn_sair.set_position(janela.width/2 - btn_sair.width/2, janela.height/2 + 225)

btn_facil.set_position(janela.width/2 - btn_facil.width/2, janela.height/2 - 150)
btn_medio.set_position(janela.width/2 - btn_medio.width/2, janela.height/2)
btn_dificil.set_position(janela.width/2 - btn_dificil.width/2, janela.height/2 + 150)

estado = "MENU"
dificuldade = 1
player = Jogador(janela)

while True:
    
    janela.set_background_color((0, 0, 0))

    if estado == "MENU":
        btn_jogar.draw()
        btn_dificuldade.draw()
        btn_ranking.draw()
        btn_sair.draw()

        if mouse.is_over_object(btn_jogar) and mouse.is_button_pressed(1):
            estado = "JOGAR"
        elif mouse.is_over_object(btn_dificuldade) and mouse.is_button_pressed(1):
            estado = "DIFICULDADE"
        elif mouse.is_over_object(btn_ranking) and mouse.is_button_pressed(1):
            pass
        elif mouse.is_over_object(btn_sair) and mouse.is_button_pressed(1):
            janela.close()

    elif estado == "JOGAR":
        player.update(dificuldade)
        player.draw()
        
        if teclado.key_pressed("ESC"):
            estado = "MENU"
            
    elif estado == "DIFICULDADE":
        btn_facil.draw()
        btn_medio.draw()
        btn_dificil.draw()
        
        if teclado.key_pressed("ESC"):
            estado = "MENU"
            
        if mouse.is_over_object(btn_facil) and mouse.is_button_pressed(1):
            dificuldade = 1
            estado = "MENU"
        elif mouse.is_over_object(btn_medio) and mouse.is_button_pressed(1):
            dificuldade = 2
            estado = "MENU"
        elif mouse.is_over_object(btn_dificil) and mouse.is_button_pressed(1):
            dificuldade = 3
            estado = "MENU"

    janela.update()