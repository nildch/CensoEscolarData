from flask import Flask, jsonify, request, abort
from db_funcoes import get_connection, get_ranking_instituicoes 
from log_config import logger


app = Flask(__name__)


@app.get("/instituicoes")
def listar_instituicoes():
    logger.info("Requisição recebida: GET /instituicoes")
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM instituicoes LIMIT 100") 
    dados = cursor.fetchall()

    conn.close()

    logger.info(f"{len(dados)} instituições retornadas")
    return jsonify([dict(linha) for linha in dados])




@app.get("/instituicoesensino/ranking/<int:ano>")
def get_ranking_route(ano):
    """
    Endpoint: /instituicoesensino/ranking/{ano}
    Retorna o ranking das 10 IEs com mais matrículas.
    """
    logger.info(f"Requisição recebida: GET /instituicoesensino/ranking/{ano}")

 
    if ano < 2022 or ano > 2024:
        logger.warning(f"Ano inválido solicitado: {ano}")
        return jsonify({"erro": "Ano inválido. O campo 'ano' deve ser entre 2022 e 2024."}), 400

   
    try:
        ranking = get_ranking_instituicoes(ano) 

        if not ranking:
             logger.warning(f"Nenhum dado encontrado para o ranking do ano {ano}.")
             return jsonify({"erro": f"Nenhum dado encontrado para o ano {ano}. Verifique a carga de dados."}), 404

        logger.info(f"Sucesso ao buscar ranking para o ano {ano}. Retornando {len(ranking)} IEs.")
        return jsonify(ranking), 200

    except Exception as e:
        logger.error(f"Erro interno ao processar ranking para o ano {ano}: {e}")
        return jsonify({"erro": "Erro interno do servidor."}), 500


if __name__ == "__main__":
    app.run(debug=True)