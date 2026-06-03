from PPlay.window import Window

janela = Window(800,600, "Straw Hat Odyssey")

while True:
    if tela == 0:
        cor(janela, "preto")
        play.draw()
        options.draw()
        exit.draw()

        if clicou_em(start):
            tela = 1
        if clicou_em(dificult):
            tela = 2
        if clicou_em(ranking):
            tela = 3
        if clicou_em(exit):
            break
