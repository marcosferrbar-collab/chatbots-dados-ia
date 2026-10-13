"""
Passo 2: Exploração dos dados com pandas.
Rode este script primeiro para entender a base antes de conectar a IA.
"""
import pandas as pd

df = pd.read_csv("vendas.csv", parse_dates=["data"])
df["valor_total"] = df["quantidade"] * df["preco_unitario"]

print("=== Primeiras linhas ===")
print(df.head())

print("\n=== Estatísticas gerais ===")
print(df.describe(include="all"))

print("\n=== Faturamento por categoria ===")
print(df.groupby("categoria")["valor_total"].sum().sort_values(ascending=False))

print("\n=== Faturamento por vendedor ===")
print(df.groupby("vendedor")["valor_total"].sum().sort_values(ascending=False))

print("\n=== Produto mais vendido (em quantidade) ===")
print(df.groupby("produto")["quantidade"].sum().sort_values(ascending=False).head(1))
