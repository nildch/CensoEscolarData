import pandas as pd

df = pd.read_csv(
    "data/microdados_ed_basica_2024.csv",
    sep=';',
    encoding='latin1',
    nrows=5
)

print("\n=== Nomes das colunas ===")
print(df.columns.tolist())

print("\n=== Primeiras linhas ===")
print(df.head())