import json
import httpx
import asyncio

import help_user


async def start_app():
    token_client = input("Informe o token do cliente: ")
    environment = input("Informe o Environment (local, homo, prd): ")
    produto = input("Informe o nome do produto: ")
    if environment == "prd":
        cliente = input("Informe o cliente: ")
    else:
        cliente = None
    request = int(input("""
    Informe a requisicao que deseja utilizar:
    1 - ativar_veiculo
    2 - inativar_veiculo
    3 - pesquisar_token
    4 - ativar_e_inativar_veiculo
    5 - Pesquisar placas:
    6 - Converter arquivo: \n
    """))

    if request == 1:
        archive = input("Informe o nome do arquivo json, não precisa colocar a extensão .json: ")
        dados = help_user.read_archive(archive)
        await process_request_active_vehicle(dados, token_client, environment, cliente, produto)
    elif request == 2:
        archive = input("Informe o nome do arquivo json, não precisa colocar a extensão .json: ")
        dados_deactivated = help_user.read_archive(archive)
        await process_request_deactivated_vehicle(dados_deactivated, token_client, environment, cliente)
    elif request == 3:
        for i in range(1, 30 + 1):
            print(f"Request number {i}")
            await post_expiration_token(token_client, environment, cliente)
    elif request == 4:
        archive_active = input("Informe o nome do arquivo json para ativação, não precisa colocar a extensão .json: ")
        archive_inactivated = input(
            "Informe o nome do arquivo json para desativação, não precisa colocar a extensão .json: ")
        dados_active = help_user.read_archive(archive_active)
        dados_inactivated = help_user.read_archive(archive_inactivated)

        await process_request_active_vehicle(dados_active, token_client, environment, cliente, produto)
        await process_request_deactivated_vehicle(dados_inactivated, token_client, environment, cliente)
    elif request == 5:
        search_plate = input("Informe o nome do arquivo json para pesquisa, não precisa colocar a extensão .json: ")
        dados_plate = help_user.read_archive(search_plate)
        await post_search_vehicle(dados_plate, token_client, environment, cliente)
    elif request == 6:
        archive_active = input("Informe o nome do arquivo json para converter, não precisa colocar a extensão .json: ")
        convert_archive(archive_active, produto)
    else:
        print("Invalid option")
        await start_app()


async def process_request_active_vehicle(dados, token_client, environment, client, produto):
    if len(dados) > 0:
        if len(dados) <= 1:
            await post_activated_vehicle(dados, token_client, environment, client)
        else:
            for j in help_user.divide_json(dados, 1, produto):
                await post_activated_vehicle(j, token_client, environment, client)


async def process_request_deactivated_vehicle(dados, token_client, environment, client):
    if len(dados) > 0:
        for i in range(0, len(dados)):
            await post_deactivated_vehicle(dados[i], token_client, environment, client)


async def post_activated_vehicle(json_file, token, environment, client):
    print('Posting activated vehicle')

    if environment == 'local':
        url = ['http://localhost:8082/synchrony/api/v2/vehicle/active']
    elif environment == 'homo':
        url = ["https://teste.teste.com.br/synchrony/api/v2/vehicle/active"]
    else:
        url = [f"https://{client}.ativo247.com.br/synchrony/api/v2/vehicle/active"]

    headers = {
        'Accept': 'application/json',
        'token': f'{token}',
        'Content-Type': 'application/json'
    }

    await request_by_token(urls=url, headers=headers, json_data=json_file)


async def post_expiration_token(token, environment, client):
    print('Posting expiration token')

    if environment == 'local':
        url = ['http://localhost:8082/synchrony/api/v2/token/expiration']
    elif environment == 'homo':
        url = ["https://teste.teste.com.br/synchrony/api/v2/token/expiration"]
    else:
        url = [f"https://{client}.ativo247.com.br/synchrony/api/v2/token/expiration"]

    headers = {
        'Accept': 'application/json',
        'token': f'{token}',
    }

    await request_by_token(url, headers, None)


async def post_deactivated_vehicle(json_file, token, environment, client):
    print('Posting deactivated vehicle')

    if environment == 'local':
        url = ["http://localhost:8082/synchrony/api/v2/vehicle/deactivate"]
    elif environment == 'homo':
        url = ["https://teste.teste.com.br/synchrony/api/v2/vehicle/deactivate"]
    else:
        url = [f"https://{client}.ativo247.com.br/synchrony/api/v2/vehicle/deactivate"]

    headers = {
            'Accept': 'application/json',
            'token': f'{token}',
            'Content-Type': 'application/json'
        }

    await request_by_token(urls=url, headers=headers, json_data=json_file)


async def post_search_vehicle(json_file, token, environment, client):
    print('Post searching vehicle')

    if environment == 'local':
        url = ['http://localhost:8082/synchrony/api/v2/vehicle/find']
    elif environment == 'homo':
        url = ["https://teste.teste.com.br/synchrony/api/v2/vehicle/find"]
    else:
        url = [f"https://{client}.ativo247.com.br/synchrony/api/v2/vehicle/find"]

    headers = {
        'Accept': 'application/json',
        'token': f'{token}',
        'Content-Type': 'application/json'
    }

    await request_by_token(urls=url, headers=headers, json_data=json_file)


async def fetch_url_with_timeout(client, url, headers, json_data, timeout=300):
    try:
        # new_json_data = json.dumps(json_data)
        response = await client.post(url=url, headers=headers, json=json_data, timeout=timeout)
        if response.status_code == 200:
            return response
        else:
            return {"error": f"Erro na solicitação: {response.text}"}
    except asyncio.exceptions.CancelledError as e:
        return {"error": f"Erro ao buscar a URL {url}, {e}"}
    except httpx.ReadTimeout as e:
        return {"error": f"Timeout ao buscar a URL {url}, {e}"}


async def request_by_token(urls, headers, json_data):
    tasks = []
    async with httpx.AsyncClient() as client:
        for url in urls:
            print(f"Link: {url}")
            task = fetch_url_with_timeout(client, url, headers, json_data if json_data is not None else None)
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

    for response in responses:
        if isinstance(response, dict) and "error" in response:
            print(response["error"])
        else:
            print("Resposta da API:", response.text)


def convert_archive(archive_name, produto):
    help_user.salvar_novo_arquivos(help_user.abrir_e_converter_arquivos(archive_name, produto))
    print('Arquivo criado')


if __name__ == '__main__':
    asyncio.run(start_app())
