from PPlay.sprite import *
from PPlay.keyboard import *
from PPlay.sprite import *
from PPlay.collision import *

keyboard = Keyboard()
velocidade_inimigo = 100

# Background do Jogo

def cor(janela, string):
    if string == "branco":
        return janela.set_background_color([0,0,0])

def Jogatina(janela, nave, tiros, velocidade, velocidade_tiro, inimigos):
    global velocidade_inimigo
    
    cor(janela, "preto")
    nave.draw()

    dt = janela.delta_time()
    deslocamento_x = velocidade_inimigo * dt
    bateu_na_parede = False
    
    menor_x = janela.width
    maior_x = 0
    menor_y = janela.height if hasattr(janela,'height') else 9999
    maior_y = 0

    tem_inimigos = False
    
    for linha in inimigos:
        for bicho in linha:
            tem_inimigos = True
            
            if bicho.x < menor_x:
                menor_x = bicho.x
            if bicho.x + bicho.width > maior_x:
                maior_x = bicho.x + bicho.width
                
            if bicho.y < menor_y:
                menor_y = bicho.y
            if bicho.y + bicho.height > maior_y:
                maior_y = bicho.y + bicho.height
                
    if tem_inimigos:
        if menor_x + deslocamento_x <= 0 or maior_x + deslocamento_x >= janela.width:
            velocidade_inimigo *= -1                   
            deslocamento_x = velocidade_inimigo * dt  
            bateu_na_parede = True                     
            
        for linha in inimigos:
            for bicho in linha:
                bicho.x += deslocamento_x
                if bateu_na_parede:
                    bicho.y += 20 
                bicho.draw()

    # Tiros
    for tiro in tiros[:]:

        if (tiro.x + tiro.width >= menor_x and tiro.x <= maior_x and tiro.y + tiro.height >= menor_y and tiro.y <= maior_y ):
            bateu = False
            for linha in reversed(inimigos):
                for bicho in linha[:]:
                    
                    if (tiro.x < bicho.x + bicho.width and tiro.x + tiro.width > bicho.x and tiro.y < bicho.y + bicho.height and tiro.y + tiro.height > bicho.y):
                        linha.remove(bicho)
                        tiros.remove(tiro)
                        bateu = True
                        break
                if bateu:
                    break


    if keyboard.key_pressed("right"):
        nave.x += velocidade * dt
    if keyboard.key_pressed("left"):
        nave.x -= velocidade * dt
        
    if nave.x < 0:
        nave.x = 0
    if nave.x > janela.width - nave.width:
        nave.x = janela.width - nave.width
        
    if keyboard.key_down("space"):
        novo_tiro = Sprite("sprites/tiro.png")
        novo_tiro.set_position(nave.x + nave.width/2 - novo_tiro.width/2, nave.y - novo_tiro.height)
        tiros.append(novo_tiro)
        
    for tiro in tiros[:]:
        tiro.draw()
        tiro.y -= velocidade_tiro * dt
        if tiro.y < 0:
            tiros.remove(tiro)