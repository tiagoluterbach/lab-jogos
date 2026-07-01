import os

ARQUIVO = "ranking.txt"


# lê o arquivo de ranking e retorna a lista ordenada
def carregar():
    lista = []
    if os.path.exists(ARQUIVO):
        f = open(ARQUIVO, "r", encoding="utf-8")
        for linha in f:
            linha = linha.strip()
            if linha == "":
                continue
            partes = linha.split(";")
            if len(partes) == 3:
                nome = partes[0]
                tempo = float(partes[1])
                resultado = partes[2]
                lista.append([nome, tempo, resultado])
        f.close()
    vitorias = []
    derrotas = []
    for item in lista:
        if item[2] == "venceu":
            vitorias.append(item)
        else:
            derrotas.append(item)
    vitorias.sort(key=lambda item: item[1])
    return vitorias + derrotas


# salva o resultado no arquivo de ranking
def salvar(nome, tempo, resultado):
    if nome == "":
        nome = "Anonimo"
    f = open(ARQUIVO, "a", encoding="utf-8")
    f.write(nome + ";" + str(round(tempo, 1)) + ";" + resultado + "\n")
    f.close()
