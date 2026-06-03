from PPlay.sprite import *

def bichinhos(janela):
    start = Sprite("sprites/start.png")
    start.set_position((janela.width/2-start.width/2),(janela.height/2-start.height/2) - 200)

    dificult = Sprite("sprites/dificult.png")
    dificult.set_position((janela.width/2-dificult.width/2),(janela.height/2-dificult.height/2) - 100)

    ranking = Sprite("sprites/ranking.png")
    ranking.set_position((janela.width/2-ranking.width/2),(janela.height/2-ranking.height/2) - 0)

    exit = Sprite("sprites/exit.png")
    exit.set_position((janela.width/2-exit.width/2),(janela.height/2-exit.height/2) + 100)

    facil = Sprite("sprites/facil.png")
    facil.set_position((janela.width/2-facil.width/2),(janela.height/2-facil.height/2) -225)

    medio = Sprite("sprites/medio.png")
    medio.set_position((janela.width/2-medio.width/2),(janela.height/2-medio.height/2) - 150)

    dificil = Sprite("sprites/dificil.png")
    dificil.set_position((janela.width/2-dificil.width/2),(janela.height/2-dificil.height/2) - 75)

    nave = Sprite("sprites/nave.png")
    nave.set_position((janela.width/2-nave.width/2),(janela.height/2-nave.height/2) + 250)

    coluna = 9
    linha = 4
    bicho = Sprite("sprites/bicho.png")
    spacing_x = bicho.width / 2
    spacing_y = bicho.height / 2
    
    inimigos = [[Sprite("sprites/bicho.png") for j in range(coluna)] for i in range(linha)]
    for i in range(linha):
        for j in range(coluna):
            x = (janela.width/2 - (coluna * bicho.width + (coluna-1) * spacing_x) / 2) + j * (bicho.width + spacing_x)
            y = 50 + i * (bicho.height + spacing_y)
            inimigos[i][j].set_position(x, y)

    
    return {
        "sprites/start": start,
        "sprites/dificult": dificult,
        "sprites/ranking": ranking,
        "sprites/exit": exit,
        "sprites/facil": facil,
        "sprites/medio": medio,
        "sprites/dificil": dificil,
        "sprites/nave": nave,
        "sprites/bicho": bicho,
        "sprites/inimigos": inimigos
    }