import sqlite3


def criar_tabela():

    conexao = sqlite3.connect("coinbase.db")

    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS precos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT,
            preco REAL,
            data_hora TEXT
        )
    """)

    conexao.commit()
    conexao.close()


def inserir_preco(produto, preco, data_hora):

    conexao = sqlite3.connect("coinbase.db")

    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO precos (produto, preco, data_hora)
        VALUES (?, ?, ?)
    """, (produto, preco, data_hora))

    conexao.commit()

    conexao.close()