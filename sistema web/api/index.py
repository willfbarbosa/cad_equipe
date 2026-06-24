from flask import Flask, render_template, request, redirect, send_file
import sqlite3
from openpyxl import Workbook
from io import BytesIO

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

def conectar():
    conn = sqlite3.connect("equipamentos.db")
    conn.row_factory = sqlite3.Row
    return conn


# 🔹 ROTAS (cole suas rotas aqui dentro igual estavam no app.py)

@app.route("/")
def index():
    conn = conectar()
    equipamentos = conn.execute("SELECT * FROM equipamentos").fetchall()
    conn.close()
    return render_template("index.html", equipamentos=equipamentos)


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    conn = conectar()

    conn.execute("""
        INSERT INTO equipamentos
        (nome, patrimonio, marca, modelo, localizacao, ip, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        request.form["nome"],
        request.form["patrimonio"],
        request.form["marca"],
        request.form["modelo"],
        request.form["localizacao"],
        request.form["ip"],
        request.form["status"]
    ))

    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/exportar_excel")
def exportar_excel():

    conn = conectar()
    equipamentos = conn.execute("SELECT * FROM equipamentos").fetchall()
    conn.close()

    wb = Workbook()
    ws = wb.active
    ws.title = "Equipamentos"

    ws.append(["ID","Nome","Patrimonio","Marca","Modelo","Localizacao","IP","Status"])

    for e in equipamentos:
        ws.append([
            e["id"], e["nome"], e["patrimonio"], e["marca"],
            e["modelo"], e["localizacao"], e["ip"], e["status"]
        ])

    arquivo = BytesIO()
    wb.save(arquivo)
    arquivo.seek(0)

    return send_file(
        arquivo,
        as_attachment=True,
        download_name="equipamentos.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# IMPORTANTE: handler para Vercel
def handler(environ, start_response):
    return app(environ, start_response)