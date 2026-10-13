# Chatbot de Vendas — Projeto prático

Projeto que une análise de dados + IA num só lugar: um chatbot que responde
perguntas em português sobre uma planilha de vendas.

## Arquivos
- `vendas.csv` — dados de exemplo (troque pelos seus próprios depois)
- `analise.py` — exploração dos dados com pandas (rode primeiro, sem precisar de API)
- `app.py` — chatbot com interface Streamlit conectado à API da Anthropic

## Passo a passo

### 1. Explore os dados (sem custo, sem API)
```bash
pip install pandas
python analise.py
```
Isso te mostra estatísticas, faturamento por categoria/vendedor etc.
Entenda a base antes de conectar a IA.

### 2. Rode o chatbot
```bash
pip install streamlit pandas anthropic
export ANTHROPIC_API_KEY="sua-chave-aqui"
streamlit run app.py
```
Crie sua chave em https://console.anthropic.com/settings/keys

Abra o navegador (o Streamlit abre sozinho) e faça perguntas como:
- "Qual vendedor teve o maior faturamento?"
- "Quantas unidades de Café 500g foram vendidas?"
- "Qual foi o produto mais vendido em janeiro?"

## Próximos passos (quando quiser evoluir)
1. **Trocar o CSV pelos seus dados reais** — mesma estrutura, dados diferentes
2. **Bases grandes**: em vez de mandar o CSV inteiro pra IA, pré-calcule
   agregados com pandas (como em `analise.py`) e mande só o resumo — isso é
   o início de uma técnica chamada RAG (Retrieval-Augmented Generation)
3. **Guardar histórico de conversas** em um banco de dados (SQLite é um bom
   começo, já que você já sabe SQL)
4. **Deploy**: o Streamlit tem hospedagem gratuita (streamlit.io/cloud) pra
   colocar isso no ar e mostrar no portfólio
