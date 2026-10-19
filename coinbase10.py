import requests


def consultar_produto(produto):

    url = f"https://api.coinbase.com/v2/prices/{produto}/spot"

    resposta = requests.get(url)

    dados = resposta.json()

    return dados
