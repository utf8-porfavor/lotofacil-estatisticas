import asyncio
import httpx

API_URL = "https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil"
CONCORRENCIA = 3
PAUSA = 0.5

async def buscar_ultimo() -> int:
    async with httpx.AsyncClient() as client:
        resposta = await client.get(API_URL, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
        return dados["numero"]

async def _buscar_concurso(client: httpx.AsyncClient, semaforo: asyncio.Semaphore, numero: int) -> list | None:
    async with semaforo:
        await asyncio.sleep(PAUSA)
        for tentativa in range(3):
            try:
                resposta = await client.get(f"{API_URL}/{numero}", timeout=10)
                resposta.raise_for_status()
                dados = resposta.json()
                dezenas = sorted(dados["listaDezenas"])
                return [f"C{numero}"] + dezenas
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    await asyncio.sleep(2 ** tentativa)
                else:
                    print(f"Erro no concurso {numero}: {e}")
                    return None
            except httpx.HTTPError as e:
                if tentativa < 2 :
                    await asyncio.sleep(2 ** tentativa)
                else:
                    print(f"Erro de conexão no concurso {numero}: {type(e).__name__} {e}")
                    return None
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
