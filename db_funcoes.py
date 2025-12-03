import sqlite3
from log_config import logger
import os


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database", "censo_escolar.db")
TABLE_NAME = 'instituicoes'

def get_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row 
    return conn

def get_ranking_instituicoes(ano: int):
    """
    Busca as 10 IEs com mais matrículas para o ano especificado,
    ordena e calcula a posição (nu_ranking) na requisição.
    """
    logger.info(f"Buscando IEs para ranking (calculo em tempo real) do ano {ano}.")
    conn = get_connection()
    
    try:
       
        query = f"""
            SELECT
                co_entidade, no_entidade, no_uf, sg_uf, co_uf, no_municipio,
                co_municipio, no_mesorregiao, co_mesorregiao, no_microrregiao,
                co_microrregiao, nu_ano_censo, no_regiao, co_regiao,
                qt_mat_bas, qt_mat_prof, qt_mat_eja, qt_mat_esp, qt_mat_fund,
                qt_mat_inf, qt_mat_med, qt_mat_zr_na, qt_mat_zr_rur,
                qt_mat_zr_urb, qt_mat_total
            FROM
                {TABLE_NAME}
            WHERE
                nu_ano_censo = ?
            ORDER BY
                qt_mat_total DESC
            LIMIT 10;
        """
        
        cursor = conn.execute(query, (ano,))
        instituicoes = cursor.fetchall()

        ranking_list = []
       
        for i, row in enumerate(instituicoes):
            item = dict(row)
            item['nu_ranking'] = i + 1 
            ranking_list.append(item)
            
        logger.info(f"Top 10 IEs encontradas para o ano {ano}.")
        return ranking_list

    except sqlite3.Error as e:
        logger.error(f"Erro SQL ao buscar ranking para o ano {ano}: {e}")
        return []
    finally:
        conn.close()

