import asyncio
import httpx

API_URL = "https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil"
CONCORRENCIA = 10
PAUSA = 0.3

async def buscar_ultimo() -> int:
    async with httpx.AsyncClient() as client:
        resposta = await client.get(API_URL, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
        return dados["numero"]

async def _buscar_concurso(client: httpx.AsyncClient, semaforo: asyncio.Semaphore, numero: int) -> list | None:
    async with semaforo:
        await asyncio.sleep(PAUSA)
        try:
            resposta = await client.get(f"{API_URL}/{numero}", timeout=10)
            resposta.raise_for_status()
            dados = resposta.json()
            dezenas = sorted(dados["listaDezenas"])
            return [f"C{numero}"] + dezenas
        except httpx.HTTPError as e:
            print(f"Erro no concurso {numero}: {e}")
            return None


async def buscar_intervalo(inicio: int, fim: int) -> list:
    semaforo = asyncio.Semaphore(CONCORRENCIA)
    async with httpx.AsyncClient() as client:
        tarefas = [
            _buscar_concurso(client, semaforo, numero)
            for numero in range(inicio, fim + 1)
        ]
        resultados = await asyncio.gather(*tarefas)

    return [r for r in resultados if r is not None]
