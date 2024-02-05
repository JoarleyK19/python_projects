import json


def converter_formato(dados_antes, produto):
    list_dict = []
    for item in dados_antes:
        list_dict.append({
            "uuid": "",
            "id": "",
            "status": "ATIVO",
            "produtos": {f"{produto}": f"{produto}"},
            "placa": item["placa"],
            "chassi": item["chassi"],
            "codigo_veiculo": "",
            "renavam": item["renavam"],
            "ano_fabricacao": item["ano_fabricacao"],
            "ano_modelo": item["ano_modelo"],
            "codigo_fipe": item["codigo_fipe"],
            "valor_fipe": item["valor_fipe"],
            "data_contrato_veiculo": "",
            "codigo_situacao": "",
            "descricao_situacao": "",
            "codigo_associado": "",
            "nome_associado": item["nome_associado"],
            "cpf": item["cpf"],
            "rg": item["rg"],
            "data_nascimento": item["data_nascimento"],
            "data_contrato_associado": "",
            "cep": item["cep"],
            "logradouro": item["logradouro"],
            "numero": item["numero"],
            "complemento": item["complemento"],
            "bairro": item["bairro"],
            "cidade": item["cidade"],
            "estado": item["estado"],
            "ddd": item["ddd"],
            "telefone": item["telefone"],
            "ddd_celular": item["ddd_celular"],
            "telefone_celular": item["telefone_celular"],
            "email": item["email"],
            "codigo_situacao_associado": "",
            "descricao_situacao_associado": "",
            "codigo_marca": "",
            "descricao_marca": item["descricao_marca"],
            "codigo_modelo": "",
            "descricao_modelo": item["descricao_modelo"],
            "codigo_cor": item["codigo_cor"],
            "descricao_cor": item["descricao_cor"],
            "codigo_tipoveiculo": "",
            "descricao_tipoveiculo": 1,
            "codigo_combustivel": "",
            "descricao_combustivel": 1,
            "codigo_cooperativa": "",
            "nome_cooperativa": "",
            "codigo_regional": "",
            "nome_regional": ""
        })

    return list_dict


def abrir_e_converter_arquivos(arquivo, produto):
    """
        Abre o arquivo JSON de entrada,
        Converte o formato
    """
    with open(f"./{arquivo}.json", 'r', encoding='utf-8') as arquivo_antes:
        dados_antes = json.load(arquivo_antes)
    dados_depois = converter_formato(dados_antes, produto)
    return dados_depois


def salvar_novo_arquivos(arquivo):
    """
        Salva o novo arquivo JSON
        recebe como parâmentro o novo arquivo para savar em json
    """
    with open('depois.json', 'w', encoding='utf-8') as arquivo_depois:
        json.dump(arquivo, arquivo_depois, indent=2, ensure_ascii=False)


def divide_json(input_file, chunk_size, produto):
    """
        Metodo usado para quebrar um arquivo json,
        Recebe como parâmentro o input_file é a quantidade de itens para ficar
        em cada arquivo json.
    """
    total_items = len(input_file)
    num_chunks = (total_items + chunk_size - 1) // chunk_size
    new_items_list = []
    for i in range(num_chunks):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size
        chunk_data = input_file[start_index:end_index]
        new_items_list.append(converter_formato(chunk_data, produto))

    return new_items_list


def read_archive(archive):
    with open(f'./{archive}.json', 'r', encoding='utf-8') as lead_archive:
        dados = json.load(lead_archive)

    return dados
