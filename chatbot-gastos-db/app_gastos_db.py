"""
Chatbot de gastos pessoais, agora consultando o banco de dados SQLite
(despesas.db) em vez de um CSV fixo — suporta vários meses.

Como rodar:
    pip3 install streamlit pandas requests
    python3 criar_banco.py       (roda uma vez, cria o banco)
    ollama run llama3.2          (ou já ter feito "ollama pull" antes)
    python3 -m streamlit run app_gastos_db.py
"""
import sqlite3
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Chatbot de Gastos (com banco)", page_icon="💶")
st.title("💶 Chatbot de Gastos Pessoais — com banco de dados")
st.caption("Agora consultando um banco SQLite, que guarda vários meses.")

@st.cache_data
def carregar_dados():
    conexao = sqlite3.connect("despesas.db")
    df = pd.read_sql("SELECT * FROM despesas", conexao)
    conexao.close()
    return df

df = carregar_dados()

with st.expander("Ver todas as despesas no banco"):
    st.dataframe(df)

def montar_resumo(dados: pd.DataFrame) -> str:
    total_geral = dados["valor_euros"].sum()
    por_mes = dados.groupby("mes")["valor_euros"].sum().round(2)
    por_categoria = (
        dados.groupby("categoria")["valor_euros"].sum().round(2)
        .sort_values(ascending=False)
    )

    linhas = [f"Total gasto (todos os meses): € {total_geral:.2f}"]
    linhas.append("\nTotal por mês:")
    for mes, valor in por_mes.items():
        linhas.append(f"- {mes}: € {valor}")
    linhas.append("\nTotal por categoria (somando todos os meses):")
    for cat, valor in por_categoria.items():
        linhas.append(f"- {cat}: € {valor}")
    return "\n".join(linhas)

def perguntar_para_ia(pergunta: str, dados: pd.DataFrame) -> str:
    resumo = montar_resumo(dados)
    prompt = (
        "Você é um assistente financeiro pessoal. Os números abaixo já "
        "foram calculados com precisão — NÃO refaça as contas, apenas leia "
        "e responda a pergunta usando esses valores exatos, em português.\n\n"
        f"Resumo das despesas:\n{resumo}\n\n"
        f"Pergunta: {pergunta}"
    )
    resposta = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False},
        timeout=300,
    )
    resposta.raise_for_status()
    return resposta.json()["response"]

if "historico" not in st.session_state:
    st.session_state.historico = []

for autor, texto in st.session_state.historico:
    with st.chat_message(autor):
        st.write(texto)

pergunta = st.chat_input("Ex: Quanto gastei em setembro?")

if pergunta:
    st.session_state.historico.append(("user", pergunta))
    with st.chat_message("user"):
        st.write(pergunta)
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resposta = perguntar_para_ia(pergunta, df)
            st.write(resposta)
    st.session_state.historico.append(("assistant", resposta))
