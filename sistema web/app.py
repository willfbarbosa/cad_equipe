from flask import Flask, render_template, request, redirect
import sqlite3
from flask import send_from_directory
app = Flask(__name__)

@app.route('/logo')
def logo():
    return send_from_directory('.', 'logo.png')
def conectar():
    conn = sqlite3.connect("equipamentos.db")
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabela():
    conn = conectar()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS equipamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            patrimonio TEXT,
            marca TEXT,
            modelo TEXT,
            localizacao TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

criar_tabela()

@app.route("/")
def index():
    conn = conectar()
    equipamentos = conn.execute(
        "SELECT * FROM equipamentos"
    ).fetchall()
    conn.close()

    return render_template(
        "index.html",
        equipamentos=equipamentos
    )

@app.route("/cadastrar", methods=["POST"])
def cadastrar():

    nome = request.form["nome"]
    patrimonio = request.form["patrimonio"]
    marca = request.form["marca"]
    modelo = request.form["modelo"]
    localizacao = request.form["localizacao"]
    status = request.form["status"]

    conn = conectar()

    conn.execute("""
        INSERT INTO equipamentos
        (nome, patrimonio, marca, modelo, localizacao, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
    (nome, patrimonio, marca, modelo, localizacao, status))

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/editar/<int:id>")
def editar(id):

    conn = conectar()

    equipamento = conn.execute(
        "SELECT * FROM equipamentos WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "editar.html",
        equipamento=equipamento
    )

@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar(id):

    conn = conectar()

    conn.execute("""
        UPDATE equipamentos
        SET nome=?,
            patrimonio=?,
            marca=?,
            modelo=?,
            localizacao=?,
            status=?
        WHERE id=?
    """, (
        request.form["nome"],
        request.form["patrimonio"],
        request.form["marca"],
        request.form["modelo"],
        request.form["localizacao"],
        request.form["status"],
        id
    ))

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/excluir/<int:id>")
def excluir(id):

    conn = conectar()

    conn.execute(
        "DELETE FROM equipamentos WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)