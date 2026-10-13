"""
Versão gratuita do chatbot, usando Ollama (modelo rodando local no PC)
em vez da API paga da Anthropic.

Como rodar:
    pip3 install streamlit pandas requests
    ollama run llama3.2   (deixe isso rodando em outro terminal, ou já
                            tenha feito "ollama pull llama3.2" antes)
    python3 -m streamlit run app_ollama.py
"""
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Chatbot de Vendas (Ollama)", page_icon="📊")
st.title("📊 Chatbot de Vendas — versão gratuita (Ollama)")
st.caption("Faça perguntas em português sobre os dados de vendas do CSV.")

# --- Carrega os dados ---
@st.cache_data
def carregar_dados():
    df = pd.read_csv("vendas.csv", parse_dates=["data"])
    df["valor_total"] = df["quantidade"] * df["preco_unitario"]
    return df

df = carregar_dados()

with st.expander("Ver dados brutos"):
    st.dataframe(df)

def perguntar_para_ia(pergunta: str, dados: pd.DataFrame) -> str:
    contexto_csv = dados.to_csv(index=False)

    prompt = (
        "Você é um analista de dados. Responda a pergunta sobre a tabela de "
        "vendas abaixo (em CSV), em português, com números exatos quando "
        "possível.\n\n"
        f"Dados (CSV):\n{contexto_csv}\n\n"
        f"Pergunta: {pergunta}"
    )

    resposta = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False},
        timeout=120,
    )
    resposta.raise_for_status()
    return resposta.json()["response"]

# --- Interface de chat ---
if "historico" not in st.session_state:
    st.session_state.historico = []

for autor, texto in st.session_state.historico:
    with st.chat_message(autor):
        st.write(texto)

pergunta = st.chat_input("Ex: Qual vendedor teve o maior faturamento?")

if pergunta:
    st.session_state.historico.append(("user", pergunta))
    with st.chat_message("user"):
        st.write(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Pensando... (pode demorar um pouco, roda no seu PC)"):
            resposta = perguntar_para_ia(pergunta, df)
            st.write(resposta)
    st.session_state.historico.append(("assistant", resposta))
