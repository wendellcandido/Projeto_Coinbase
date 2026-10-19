import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Coinbase - Monitor", page_icon="$", layout="wide")

st.title("Monitor de Criptomoedas")
st.write("Visualização dos dados coletados da API da Coinbase")


@st.cache_data(ttl=60)  # recarrega no máximo a cada 60 segundos
def carregar_dados():
    conexao = sqlite3.connect("coinbase.db")
    try:
        df = pd.read_sql_query(
            "SELECT produto, preco, data_hora FROM precos ORDER BY data_hora",
            conexao,
        )
    finally:
        conexao.close()
    df["data_hora"] = pd.to_datetime(df["data_hora"])
    df["preco"] = pd.to_numeric(df["preco"], errors="coerce")
    return df


try:
    df = carregar_dados()
except Exception as erro:
    st.error(f"Não foi possível ler o banco de dados: {erro}")
    st.stop()

if df.empty:
    st.warning("Ainda não existem dados no banco.")
    st.stop()

produtos = df["produto"].unique()

# ---------------- Resumo ----------------
st.subheader("Resumo das criptomoedas")

for coluna, produto in zip(st.columns(len(produtos)), produtos):
    precos = df.loc[df["produto"] == produto, "preco"]

    atual = precos.iloc[-1]
    anterior = precos.iloc[-2] if len(precos) > 1 else None
    delta = f"{atual - anterior:,.2f}" if anterior is not None else None

    with coluna:
        st.metric(produto, f"$ {atual:,.2f}", delta=delta)
        st.write(f"Maior preço: **$ {precos.max():,.2f}**")
        st.write(f"Menor preço: **$ {precos.min():,.2f}**")

st.divider()

# ---------------- Análise detalhada ----------------
st.subheader("Análise da criptomoeda")

produto_selecionado = st.selectbox(
    "Selecione a criptomoeda para análise detalhada:", produtos
)

dados_produto = df[df["produto"] == produto_selecionado]

st.subheader(f"Histórico de preços - {produto_selecionado}")
st.line_chart(dados_produto.set_index("data_hora")["preco"])

st.divider()

st.subheader(f"Dados coletados - {produto_selecionado}")
st.dataframe(dados_produto, width="stretch")