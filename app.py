import pandas as pd
import sqlite3

CSV_PATH = "data/microdados_ed_basica_2024.csv"
DB_NAME = "censo_escolar.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS escolas (
    id_escola INTEGER PRIMARY KEY,
    nome_escola TEXT,
    regiao TEXT,
    uf TEXT,
    municipio TEXT,
    dependencia TEXT,
    etapa_ensino TEXT,
    qt_matriculas REAL
)
""")
conn.commit()

chunk_size = 10000
chunks = pd.read_csv(CSV_PATH, sep=';', encoding='latin1', chunksize=chunk_size)

for i, chunk in enumerate(chunks):
    
    # escolas paraiba, nordeste.
    chunk = chunk[(chunk['NO_REGIAO'] == 'Nordeste') & (chunk['NO_UF'] == 'Paraíba')]

    if chunk.empty:
        continue

    colunas_existentes = [c for c in ['CO_ENTIDADE', 'NO_ENTIDADE', 'NO_REGIAO', 'NO_UF', 'NO_MUNICIPIO', 'TP_DEPENDENCIA', 'TP_ETAPA_ENSINO', 'QT_MAT_BAS'] if c in chunk.columns]

    dados = chunk[colunas_existentes].copy()

    renomear = {
        'CO_ENTIDADE': 'id_escola',
        'NO_ENTIDADE': 'nome_escola',
        'NO_REGIAO': 'regiao',
        'NO_UF': 'uf',
        'NO_MUNICIPIO': 'municipio',
        'TP_DEPENDENCIA': 'dependencia',
        'TP_ETAPA_ENSINO': 'etapa_ensino',
        'QT_MAT_BAS': 'qt_matriculas'
    }
    dados.rename(columns=renomear, inplace=True)
    dados.to_sql('escolas', conn, if_exists='append', index=False)
    print(f"✅ Chunk {i+1} inserido ({len(dados)} registros da Paraíba).")

conn.close()
print("\nMigração concluída!")