import csv
from pathlib import Path

ARQUIVO_CSV = "resultados.csv"


def ler_resultados() -> list:
    if not Path(ARQUIVO_CSV).exists():
        return []

    with open(ARQUIVO_CSV, newline="") as arquivo:
        leitor = csv.reader(arquivo)
        return [linha for linha in leitor if linha]


def ultimo_concurso_salvo() -> int:
    resultados = ler_resultados()
    if not resultados:
        return 0

    ultimo = resultados[-1][0]
    return int(ultimo[1:])


def salvar_resultados(novos: list) -> None:
    existentes = ler_resultados()
    todos = existentes + novos
    todos.sort(key=lambda linha: int(linha[0][1:]))  # Ordena pelo número do concurso em forma decrescente

    with open(ARQUIVO_CSV, "w", newline="") as arquivo:
        csv.writer(arquivo).writerows(todos)
