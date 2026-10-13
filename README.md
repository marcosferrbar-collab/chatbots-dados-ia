# 🤖 Chatbots de Dados com IA

Projetos práticos combinando **análise de dados** (Python, pandas, SQL) com
**inteligência artificial** (chatbots que respondem perguntas em português
sobre dados reais), rodando com IA local e gratuita via [Ollama](https://ollama.com).

## 📁 Projetos

### 1. [`chatbot-vendas/`](./chatbot-vendas)
Chatbot que responde perguntas sobre dados de vendas (faturamento por
categoria, vendedor, produto mais vendido).
- `vendas.csv` — dados de exemplo
- `analise.py` — exploração dos dados com pandas
- `app_ollama.py` — interface do chatbot (Streamlit + Ollama)

### 2. [`chatbot-gastos/`](./chatbot-gastos)
Chatbot sobre despesas pessoais mensais (aluguel, alimentação, internet,
combustível).
- `despesas.csv` — dados de despesas
- `analise_gastos.py` — exploração com pandas
- `app_gastos.py` — interface do chatbot

### 3. [`chatbot-gastos-db/`](./chatbot-gastos-db)
Evolução do projeto de gastos, agora usando um **banco de dados SQLite**
em vez de CSV fixo, com suporte a múltiplos meses.
- `criar_banco.py` — cria e popula o banco
- `consultas_sql.py` — exemplos de consultas SQL
- `exercicios_sql.py` — exercícios práticos (INSERT, UPDATE, DELETE, JOIN, HAVING)
- `app_gastos_db.py` — chatbot conectado ao banco

## 🛠️ Tecnologias
- **Python** — linguagem principal
- **pandas** — manipulação e análise de dados
- **SQLite** — banco de dados
- **Streamlit** — interface web
- **Ollama (Llama 3.2)** — modelo de IA rodando localmente, sem custo

## 💡 Conceitos aplicados
- Pré-cálculo de agregações com pandas antes de enviar para a IA, evitando
  erros de cálculo (princípio de **RAG — Retrieval-Augmented Generation**)
- Consultas SQL: `SELECT`, `GROUP BY`, `WHERE`, `HAVING`, `JOIN`,
  `INSERT`, `UPDATE`, `DELETE`
- Integração entre uma aplicação Python e um modelo de IA local via API REST

## 🚀 Como rodar qualquer um dos projetos
```bash
pip3 install streamlit pandas requests
ollama pull llama3.2
cd nome-da-pasta-do-projeto
python3 -m streamlit run app_*.py
```

---
*Projetos desenvolvidos como parte de um processo de aprendizado prático em
dados e IA.*
