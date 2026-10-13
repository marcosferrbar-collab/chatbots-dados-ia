"""
Passo 1: Cria o banco de dados SQLite e importa as despesas do CSV.
Rode este script uma vez pra criar o banco (despesas.db).

Depois disso, você pode rodar de novo pra adicionar novos meses:
basta editar o CSV com as despesas do mês novo e rodar este script.
"""
import sqlite3
import pandas as pd

# Conecta (cria o arquivo despesas.db se não existir)
conexao = sqlite3.connect("despesas.db")

# Cria a tabela, caso ainda não exista
conexao.execute("""
    CREATE TABLE IF NOT EXISTS despesas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mes TEXT,
        categoria TEXT,
        valor_euros REAL
    )
""")

# Lê o CSV e importa pro banco
df = pd.read_csv("despesas.csv")
df.to_sql("despesas", conexao, if_exists="append", index=False)

conexao.commit()

# Confere o que foi importado
print("=== Dados no banco ===")
resultado = conexao.execute("SELECT * FROM despesas").fetchall()
for linha in resultado:
    print(linha)

conexao.close()
print(f"\n✅ {len(df)} linhas importadas para despesas.db")
