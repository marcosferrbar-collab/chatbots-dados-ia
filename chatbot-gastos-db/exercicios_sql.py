"""
Exercícios práticos de SQL, usando seu banco despesas.db.
Rode cada bloco separadamente (comente/descomente conforme for praticando),
ou rode tudo de uma vez pra ver os resultados.

Antes de começar: certifique-se de ter rodado "criar_banco.py" antes,
pra ter o despesas.db pronto.
"""
import sqlite3

conexao = sqlite3.connect("despesas.db")
cursor = conexao.cursor()

print("=" * 50)
print("EXERCÍCIO 1: INSERT — adicionar uma despesa nova")
print("=" * 50)
cursor.execute("""
    INSERT INTO despesas (mes, categoria, valor_euros)
    VALUES ('2026-10', 'Academia', 40.00)
""")
conexao.commit()
print("Despesa de Academia (outubro) adicionada!")
cursor.execute("SELECT * FROM despesas WHERE categoria = 'Academia'")
print(cursor.fetchall())

print("\n" + "=" * 50)
print("EXERCÍCIO 2: UPDATE — corrigir um valor")
print("=" * 50)
cursor.execute("""
    UPDATE despesas
    SET valor_euros = 45.00
    WHERE categoria = 'Academia' AND mes = '2026-10'
""")
conexao.commit()
print("Valor da Academia corrigido para 45€")
cursor.execute("SELECT * FROM despesas WHERE categoria = 'Academia'")
print(cursor.fetchall())

print("\n" + "=" * 50)
print("EXERCÍCIO 3: DELETE — remover uma despesa")
print("=" * 50)
cursor.execute("""
    DELETE FROM despesas
    WHERE categoria = 'Academia' AND mes = '2026-10'
""")
conexao.commit()
print("Despesa de Academia removida.")
cursor.execute("SELECT * FROM despesas WHERE categoria = 'Academia'")
print(f"Restam: {cursor.fetchall()}")

print("\n" + "=" * 50)
print("EXERCÍCIO 4: Funções de agregação (AVG, COUNT, MAX, MIN)")
print("=" * 50)
cursor.execute("SELECT AVG(valor_euros) FROM despesas")
print(f"Média de gasto por categoria: € {cursor.fetchone()[0]:.2f}")

cursor.execute("SELECT COUNT(*) FROM despesas")
print(f"Total de despesas registradas: {cursor.fetchone()[0]}")

cursor.execute("SELECT MAX(valor_euros), MIN(valor_euros) FROM despesas")
maior, menor = cursor.fetchone()
print(f"Maior despesa: € {maior:.2f} | Menor despesa: € {menor:.2f}")

print("\n" + "=" * 50)
print("EXERCÍCIO 5: HAVING — filtrar depois de agrupar")
print("=" * 50)
cursor.execute("""
    SELECT categoria, SUM(valor_euros) as total
    FROM despesas
    GROUP BY categoria
    HAVING total > 100
    ORDER BY total DESC
""")
print("Categorias com gasto total acima de 100€:")
for categoria, total in cursor.fetchall():
    print(f"- {categoria}: € {total:.2f}")

print("\n" + "=" * 50)
print("EXERCÍCIO 6: LIKE — buscar por texto parecido")
print("=" * 50)
cursor.execute("""
    SELECT * FROM despesas WHERE categoria LIKE '%Alimenta%'
""")
print(cursor.fetchall())

print("\n" + "=" * 50)
print("EXERCÍCIO 7: JOIN — comparar com metas de economia")
print("=" * 50)
# Cria uma tabela de metas (só pra praticar JOIN)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS metas (
        categoria TEXT PRIMARY KEY,
        limite_euros REAL
    )
""")
cursor.execute("DELETE FROM metas")  # limpa antes de inserir, pra poder rodar de novo
cursor.executemany("""
    INSERT INTO metas (categoria, limite_euros) VALUES (?, ?)
""", [
    ("Alimentação", 250.00),
    ("Internet", 70.00),
    ("Combustível", 120.00),
    ("Aluguel", 400.00),
    ("Compras aleatórias", 80.00),
])
conexao.commit()

cursor.execute("""
    SELECT despesas.categoria, despesas.valor_euros, metas.limite_euros,
           (despesas.valor_euros - metas.limite_euros) as diferenca
    FROM despesas
    JOIN metas ON despesas.categoria = metas.categoria
    ORDER BY diferenca DESC
""")
print("Categoria | Gasto real | Meta | Diferença (positivo = passou da meta)")
for categoria, gasto, meta, diferenca in cursor.fetchall():
    status = "⚠️ acima da meta" if diferenca > 0 else "✅ dentro da meta"
    print(f"{categoria}: € {gasto:.2f} vs € {meta:.2f} → {status}")

conexao.close()
