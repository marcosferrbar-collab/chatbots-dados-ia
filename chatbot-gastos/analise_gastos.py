"""
Análise das suas despesas pessoais com pandas.
Rode este script primeiro pra conferir os números antes de usar o chatbot.
"""
import pandas as pd

df = pd.read_csv("despesas.csv")

print("=== Despesas do mês ===")
print(df)

print(f"\n=== Total gasto no mês ===")
print(f"€ {df['valor_euros'].sum():.2f}")

print("\n=== Despesas ordenadas (maior para menor) ===")
print(df.sort_values("valor_euros", ascending=False).to_string(index=False))

print("\n=== Percentual de cada categoria no total ===")
df["percentual"] = (df["valor_euros"] / df["valor_euros"].sum() * 100).round(1)
print(df[["categoria", "valor_euros", "percentual"]].to_string(index=False))
