"""
Passo 2: Pratique SQL de verdade consultando o banco de despesas.
"""
import sqlite3

conexao = sqlite3.connect("despesas.db")
cursor = conexao.cursor()

print("=== Total gasto por mês ===")
cursor.execute("""
    SELECT mes, SUM(valor_euros) as total
    FROM despesas
    GROUP BY mes
    ORDER BY mes
""")
for mes, total in cursor.fetchall():
    print(f"{mes}: € {total:.2f}")

print("\n=== Total gasto por categoria (todos os meses) ===")
cursor.execute("""
    SELECT categoria, SUM(valor_euros) as total
    FROM despesas
    GROUP BY categoria
    ORDER BY total DESC
""")
for categoria, total in cursor.fetchall():
    print(f"{categoria}: € {total:.2f}")

print("\n=== Despesas acima de 100€ ===")
cursor.execute("""
    SELECT mes, categoria, valor_euros
    FROM despesas
    WHERE valor_euros > 100
    ORDER BY valor_euros DESC
""")
for mes, categoria, valor in cursor.fetchall():
    print(f"{mes} | {categoria}: € {valor:.2f}")

conexao.close()
