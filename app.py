from flask import Flask, jsonify, request
from db import get_connection

app = Flask(__name__)


# lista as escolas
@app.get("/escolas")
def listar_escolas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM escolas")
    dados = cursor.fetchall()

    conn.close()
    return jsonify([dict(linha) for linha in dados])



# buscar escola por ID
@app.get("/escolas/<int:id_escola>")
def buscar_por_id(id_escola):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM escolas WHERE id_escola = ?", (id_escola,))
    dado = cursor.fetchone()

    conn.close()

    if dado:
        return jsonify(dict(dado))
    return jsonify({"erro": "Escola não encontrada."}), 404


# filtrar por município
@app.get("/municipios/<nome>")
def filtrar_por_municipio(nome):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM escolas WHERE municipio LIKE ?",
        (f"%{nome}%",)
    )
    dados = cursor.fetchall()

    conn.close()
    return jsonify([dict(l) for l in dados])



# cria 1 nova escola
@app.post("/escolas")
def criar_escola():
    dados = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO escolas (id_escola, nome_escola, regiao, uf, municipio, dependencia, etapa_ensino, qt_matriculas)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dados["id_escola"],
        dados["nome_escola"],
        dados["regiao"],
        dados["uf"],
        dados["municipio"],
        dados["dependencia"],
        dados["etapa_ensino"],
        dados["qt_matriculas"]
    ))

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Escola adicionada!"}), 201



# put
@app.put("/escolas/<int:id_escola>")
def atualizar(id_escola):
    dados = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE escolas SET
            nome_escola = ?,
            regiao = ?,
            uf = ?,
            municipio = ?,
            dependencia = ?,
            etapa_ensino = ?,
            qt_matriculas = ?
        WHERE id_escola = ?
    """, (
        dados["nome_escola"],
        dados["regiao"],
        dados["uf"],
        dados["municipio"],
        dados["dependencia"],
        dados["etapa_ensino"],
        dados["qt_matriculas"],
        id_escola
    ))

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Escola atualizada!"})



#delete
@app.delete("/escolas/<int:id_escola>")
def deletar(id_escola):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM escolas WHERE id_escola = ?", (id_escola,))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Escola removida!"})


if __name__ == "__main__":
    app.run(debug=True)