"""
Chatbot de gastos pessoais, usando Ollama (gratuito, local).

Como rodar:
    pip3 install streamlit pandas requests
    ollama run llama3.2   (ou já ter feito "ollama pull llama3.2" antes)
    python3 -m streamlit run app_gastos.py
"""
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Chatbot de Gastos", page_icon="💶")
st.title("💶 Chatbot de Gastos Pessoais")
st.caption("Faça perguntas em português sobre suas despesas do mês.")

@st.cache_data
def carregar_dados():
    return pd.read_csv("despesas.csv")

df = carregar_dados()

with st.expander("Ver despesas"):
    st.dataframe(df)

def montar_resumo(dados: pd.DataFrame) -> str:
    total = dados["valor_euros"].sum()
    linhas = [f"Total gasto no mês: € {total:.2f}", "\nDespesas por categoria:"]
    for _, linha in dados.sort_values("valor_euros", ascending=False).iterrows():
        percentual = linha["valor_euros"] / total * 100
        linhas.append(
            f"- {linha['categoria']}: € {linha['valor_euros']:.2f} "
            f"({percentual:.1f}% do total)"
        )
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

pergunta = st.chat_input("Ex: Quanto gasto com alimentação?")

if pergunta:
    st.session_state.historico.append(("user", pergunta))
    with st.chat_message("user"):
        st.write(pergunta)
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resposta = perguntar_para_ia(pergunta, df)
            st.write(resposta)
    st.session_state.historico.append(("assistant", resposta))
