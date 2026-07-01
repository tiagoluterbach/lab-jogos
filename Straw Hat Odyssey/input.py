import pygame
from PPlay.window import Window


# retorna o objeto de teclado
def teclado():
    return Window.get_instance().keyboard


# retorna o objeto de mouse
def mouse():
    return Window.get_instance().mouse


# verifica se o jogador está indo para a esquerda
def esquerda():
    t = teclado()
    return t.key_pressed("a") or t.key_pressed("left")


# verifica se o jogador está indo para a direita
def direita():
    t = teclado()
    return t.key_pressed("d") or t.key_pressed("right")


# verifica se o jogador está agachando
def agachar():
    t = teclado()
    return t.key_pressed("s") or t.key_pressed("down")


# verifica se o jogador apertou o botão de pular
def pulou():
    t = teclado()
    return t.key_down("w") or t.key_down("space") or t.key_down("up")


# verifica se o jogador apertou o botão de socar
def socou():
    return teclado().key_down("j")


# verifica se o jogador apertou o botão de confirmar
def confirmou():
    return teclado().key_down("enter")


# verifica se o jogador apertou o botão de voltar/pausar
def voltar():
    return teclado().key_down("esc")


# verifica se o botão esquerdo do mouse foi clicado
def clicou():
    return mouse().button_down(1)


# retorna a posição atual do mouse
def pos_mouse():
    return mouse().get_position()


# lê os eventos do teclado e atualiza o texto digitado
def digitar(texto):
    janela = Window.get_instance()
    pronto = False
    for ev in janela.eventos:
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                pronto = True
            elif ev.key == pygame.K_BACKSPACE:
                texto = texto[:-1]
            elif ev.unicode and ev.unicode.isprintable() and len(texto) < 10:
                texto = texto + ev.unicode
    return texto, pronto
