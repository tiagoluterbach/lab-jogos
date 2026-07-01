import pygame
from PPlay.sound import Music, SoundManager
import config

MUSICA_MENU = config.caminho("musica_menu.mp3")
MUSICA_AVENTURA = config.caminho("musica_aventura.mp3")
MUSICA_BOSS = config.caminho("musica_boss.mp3")

_atual = None

# inicializa o mixer e define o volume da música
SoundManager.inicializar()
SoundManager.set_music_volume(60)


# toca a música do menu com fade
def tocar_menu():
    global _atual
    if _atual == "menu":
        return
    if _atual is not None:
        pygame.mixer.music.fadeout(800)
    _atual = "menu"
    musica = Music(MUSICA_MENU)
    musica.play(loops=-1, fade_in_ms=2000)


# toca a música da fase de aventura com fade
def tocar_aventura():
    global _atual
    if _atual == "aventura":
        return
    if _atual is not None:
        pygame.mixer.music.fadeout(800)
    _atual = "aventura"
    musica = Music(MUSICA_AVENTURA)
    musica.play(loops=-1, fade_in_ms=2000)


# toca a música da batalha do boss com fade
def tocar_boss():
    global _atual
    if _atual == "boss":
        return
    pygame.mixer.music.fadeout(800)
    _atual = "boss"
    musica = Music(MUSICA_BOSS)
    musica.play(loops=-1, fade_in_ms=1500)


# para a música com fade out
def parar(fade_ms=1000):
    global _atual
    _atual = None
    pygame.mixer.music.fadeout(fade_ms)
