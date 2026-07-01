LARGURA = 960
ALTURA = 540

PASTA = "Assets"
FONTE = PASTA + "/PirataOne-Regular.ttf"

GRAVIDADE = 1400
VEL_ANDAR = 230
FORCA_PULO = 560

dificuldade = "Medio"

cooldown_inimigo = {"Facil": 2.4, "Medio": 1.5, "Dificil": 0.8}
cooldown_boss = {"Facil": 2.6, "Medio": 1.7, "Dificil": 1.0}
preview_tempo = {"Facil": 0.95, "Medio": 0.6, "Dificil": 0.35}


def caminho(nome):
    return PASTA + "/" + nome
