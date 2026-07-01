from PPlay.window import Window
import config
from menu import Menu
from game import Jogo
import musica

janela = Window(config.LARGURA, config.ALTURA, "Straw Hat Odyssey")

menu = Menu()
jogo = None
estado = "menu"
musica.tocar_menu()

while True:
    janela.set_background_color((18, 22, 38))

    if estado == "menu":
        comando = menu.atualizar()
        if comando == "jogar":
            jogo = Jogo()
            musica.tocar_aventura()
            estado = "jogo"
        elif comando == "sair":
            janela.close()
    elif estado == "jogo":
        resultado_jogo = jogo.atualizar()
        jogo.desenhar()
        if resultado_jogo == "menu":
            musica.tocar_menu()
            menu = Menu()
            menu.tela = "principal"
            jogo = None
            estado = "menu"
        elif jogo.terminou:
            musica.tocar_menu()
            menu.iniciar_nome(jogo.resultado, jogo.tempo)
            estado = "menu"

    janela.update()
