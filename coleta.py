from datetime import datetime

from coinbase import consultar_produto
from banco import criar_tabela, inserir_preco


criar_tabela()


produtos = [
    "BTC-USD",
    "ETH-USD",
    "SOL-USD"
]


for produto in produtos:

    dados = consultar_produto(produto)

    preco = float(dados["data"]["amount"])

    data_hora = datetime.now()

    inserir_preco(produto, preco, data_hora)

    print("Produto:", produto)
    print("Preço:", preco)
    print("Data e hora:", data_hora)
    print("------------------------")


print("Todos os produtos foram coletados!")