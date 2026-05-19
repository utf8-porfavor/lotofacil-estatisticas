from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

DEZENAS = [f"{n:02d}" for n in range(1, 26)]


def gera_tabela(resultados: list) -> None:
    #tabela = Table(box=box.SIMPLE, show_footer=False)
    tabela = Table(box=box.ASCII, show_footer=False)

    tabela.add_column("Concurso", style="bold white")
    for dezena in DEZENAS:
        tabela.add_column(str(int(dezena)), justify="center")

    for concurso in resultados:
        linha = []
        for dezena in DEZENAS:
            if dezena in concurso:
                linha.append(dezena)
            else:
                linha.append("[dim]-[/dim]")
        tabela.add_row(concurso[0], *linha)

    tabela.add_section()

    porcentagens = ["%"]
    for dezena in DEZENAS:
        contador = sum(1 for linha in resultados if dezena in linha)
        porcentagem = round((contador / len(resultados)) * 100)
        porcentagens.append(f"[yellow]{porcentagem}%[/yellow]")
    tabela.add_row(*porcentagens)

    console.print(tabela)
