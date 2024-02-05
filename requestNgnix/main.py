import asyncio

import httpx


async def init_app():
    url = 'https://homologacao.ativo247.com.br/synchrony/swagger-ui/index.html#/'
    for i in range(1, 30 + 1):
        print(f'Request number: {i}')
        await request_by_token([url])  # Coloque a URL dentro de uma lista
        # Não há necessidade de incrementar i novamente aqui


async def fetch_url_with_timeout(client, url, timeout=300):
    try:
        response = await client.get(url=url, timeout=timeout)
        if response.status_code == 200:
            return response.url
        else:
            return {"error": f"Erro na solicitação: {response}"}
    except asyncio.exceptions.CancelledError as e:
        return {"error": f"Erro ao buscar a URL {url}, {e}"}
    except httpx.ReadTimeout as e:
        return {"error": f"Timeout ao buscar a URL {url}, {e}"}


async def request_by_token(urls):
    tasks = []
    async with httpx.AsyncClient() as client:
        for url in urls:
            print(f"Link: {url}")
            task = fetch_url_with_timeout(client, url)
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

    for response in responses:
        if isinstance(response, dict) and "error" in response:
            print(response["error"])
        else:
            print("Resposta da API:", response)


if __name__ == '__main__':
    asyncio.run(init_app())
