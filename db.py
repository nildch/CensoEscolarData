import sqlite3
import pandas as pd
import os
from log_config import logger 


TABLE_NAME = 'instituicoes' 
DB_PATH = "database/censo_escolar.db"
DATA_DIR = "data"
CHUNK_SIZE = 10000

ARQUIVOS = {
    2022: "microdados_ed_basica_2022.csv",
    2023: "microdados_ed_basica_2023.csv",
    2024: "microdados_ed_basica_2024.csv"
}

def criar_tabela():
    logger.info(f"Criando tabela '{TABLE_NAME}' (se não existir)")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        co_entidade INTEGER,
        no_entidade TEXT,
        no_uf TEXT,
        sg_uf TEXT,
        co_uf INTEGER,
        no_municipio TEXT,
        co_municipio INTEGER,
        no_mesorregiao TEXT,
        co_mesorregiao INTEGER,
        no_microrregiao TEXT,
        co_microrregiao INTEGER,
        nu_ano_censo INTEGER,
        no_regiao TEXT,
        co_regiao INTEGER,
        qt_mat_bas INTEGER,
        qt_mat_prof INTEGER,
        qt_mat_eja INTEGER,
        qt_mat_esp INTEGER,
        qt_mat_fund INTEGER,
        qt_mat_inf INTEGER,
        qt_mat_med INTEGER,
        qt_mat_zr_na INTEGER,
        qt_mat_zr_rur INTEGER,
        qt_mat_zr_urb INTEGER,
        qt_mat_total INTEGER -- Campo COMPUTADO na CARGA
    )
    """)
    conn.commit()
    conn.close()
    logger.info("Tabela criada ou já existente.")


def carregar_ano(ano, arquivo):
    logger.info(f"Iniciando carga do ano {ano}: arquivo {arquivo}")

    csv_path = os.path.join(DATA_DIR, arquivo)
    if not os.path.exists(csv_path):
        logger.error(f"Arquivo não encontrado: {csv_path}")
        return

    conn = sqlite3.connect(DB_PATH)
    
    
    conn.execute(f"DELETE FROM {TABLE_NAME} WHERE nu_ano_censo = {ano}")
    conn.commit()

    chunks = pd.read_csv(csv_path, sep=';', encoding='latin1', chunksize=CHUNK_SIZE, low_memory=False)

    for i, chunk in enumerate(chunks):
        logger.info(f"Processando chunk {i+1} do ano {ano}")

        
        colunas_base = [
            "CO_ENTIDADE","NO_ENTIDADE","NO_UF","SG_UF","CO_UF",
            "NO_MUNICIPIO","CO_MUNICIPIO","NO_MESORREGIAO","CO_MESORREGIAO",
            "NO_MICRORREGIAO","CO_MICRORREGIAO","NU_ANO_CENSO",
            "NO_REGIAO","CO_REGIAO"
        ]
        colunas_mat = [
            "QT_MAT_BAS","QT_MAT_PROF","QT_MAT_EJA","QT_MAT_ESP",
            "QT_MAT_FUND","QT_MAT_INF","QT_MAT_MED",
            "QT_MAT_ZR_NA","QT_MAT_ZR_RUR","QT_MAT_ZR_URB"
        ]

        # Combina colunas existentes no chunk
        colunas_existentes = [col for col in colunas_base + colunas_mat if col in chunk.columns]
        
        chunk = chunk[colunas_existentes]
        
        # Cria a lista de colunas para somar (todas que começam com QT_MAT_)
        mat_cols_to_sum = [col for col in chunk.columns if col.startswith("QT_MAT_")]

        # Calcula 'qt_mat_total'
        chunk["qt_mat_total"] = chunk[mat_cols_to_sum].fillna(0).sum(axis=1)
        
        # Renomeia todas as colunas para minúsculas
        chunk.columns = chunk.columns.str.lower()
        
        # Insere no banco
        chunk.to_sql(TABLE_NAME, conn, if_exists="append", index=False)

    conn.close()
    logger.info(f"Carga finalizada para ano {ano}!")


if __name__ == "__main__":
    criar_tabela()

    for ano, arquivo in ARQUIVOS.items():
        carregar_ano(ano, arquivo)

    logger.info("Carga feita!")
    print("\n🎉 Carga finalizada!")