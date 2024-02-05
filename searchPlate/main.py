import httpx
import asyncio
import pandas as pd


async def start_app(token: str = None):
    print(f"Token: {token}")
    if token is not None:
        q = input("Deseja utilizar o mesmo token? (S/N) ")
        if q in ('S', 's', 'sim', 'Sim'):
            headers = {
                "Authorization": f"{token}"
            }
        else:
            token = input("Informe o token: ")
            headers = {
                "Authorization": f"Bearer {token}"
            }
    else:
        token = input("Informe o token: ")
        headers = {
            "Authorization": f"Bearer {token}"
        }

    urls = open_sheet()
    await request_by_token(urls, headers)


def open_sheet():
    opc = int(input("Vai analisar uma planilha ou vai digitar a placa? (1-planilha/2-placa) "))
    if opc == 1:
        name_file = input("Informe o nome do arquivo: ")
        url_list = list()
        sheet = pd.read_excel(name_file)
        print(sheet[['placa']])
        for i in sheet.index:
            plate = sheet.loc[i, "placa"]
            url = f"https://api.hinova.com.br/api/sga/v2/sincronismo-produto-fornecedor/buscar/placa/{plate}"
            url_list.append(url)
        return url_list
    else:
        plate_client = input("Digite a placa: ")
        url = f"https://api.hinova.com.br/api/sga/v2/sincronismo-produto-fornecedor/buscar/placa/{plate_client}"
        return [url]


async def fetch_url_with_timeout(client, url, headers, timeout=300):
    try:
        response = await client.get(url=url, headers=headers, timeout=timeout)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Erro na solicitação: {response.status_code}"}
    except asyncio.exceptions.CancelledError as e:
        return {"error": f"Erro ao buscar a URL {url}, {e}"}
    except httpx.ReadTimeout as e:
        return {"error": f"Timeout ao buscar a URL {url}, {e}"}


async def request_by_token(urls, headers):
    tasks = []
    async with httpx.AsyncClient() as client:
        for url in urls:
            print(f"Link: {url}")
            task = fetch_url_with_timeout(client, url, headers)
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

    for response in responses:
        if "error" in response:
            print(response["error"])
        else:
            print("Resposta da API:", response)


if __name__ == '__main__':
    asyncio.run(start_app())
