import asyncio
import questionary
from busca import buscar_ultimo, buscar_intervalo
from salva import ler_resultados, ultimo_concurso_salvo, salvar_resultados
from gera import gera_tabela


async def atualizar():
    ultimo_api = await buscar_ultimo()
    ultimo_csv = ultimo_concurso_salvo()

    if ultimo_csv == ultimo_api:
        print("CSV já está atualizado.")
        return

    print(f"Baixando concursos {ultimo_csv + 1} até {ultimo_api}...")
    novos = await buscar_intervalo(ultimo_csv + 1, ultimo_api)
    salvar_resultados(novos)
    print(f"{len(novos)} concursos salvos.")


async def main():
    ultimo_api = await buscar_ultimo()
    ultimo_csv = ultimo_concurso_salvo()

    if ultimo_csv < ultimo_api:
        print(f"CSV desatualizado. Último concurso salvo: {ultimo_csv} | Último concurso disponível: {ultimo_api}")
        #confirma = await questionary.confirm("Deseja atualizar agora?").ask_async()
        confirma = await questionary.select("Deseja atualizar agora?",choices=["Sim", "Não"]).ask_async()
        if confirma == "Sim":
            await atualizar()

    opcao = None
    while opcao != "Sair":
        opcao = await questionary.rawselect(
            "O que você quer ver?",
            choices=[
                "Últimos 10 resultados",
                "Últimos 20 resultados",
                "Últimos X resultados",
                "Atualizar resultados",
                "Sair",
            ]
        ).ask_async()

        resultados = ler_resultados()

        if opcao == "Últimos 10 resultados":
            gera_tabela(resultados[-10:])

        elif opcao == "Últimos 20 resultados":
            gera_tabela(resultados[-20:])

        elif opcao == "Últimos X resultados":
            qtde = int(await questionary.text("Quantos resultados?").ask_async())
            gera_tabela(resultados[-qtde:])

        elif opcao == "Atualizar resultados":
            await atualizar()


if __name__ == "__main__":
    asyncio.run(main())