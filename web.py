from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "1234"

# ================= CONEXÃO =================
def get_db_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "database.db")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        conexao = get_db_connection()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT tipo FROM usuarios WHERE login = ? AND senha = ?",
            (usuario, senha)
        )
        resultado = cursor.fetchone()
        conexao.close()

        if resultado:
            session["usuario"] = usuario
            session["tipo"] = resultado["tipo"]

            if resultado["tipo"] == "usuario":
                return redirect(url_for("abrir_chamado"))
            elif resultado["tipo"] == "tecnico":
                return redirect(url_for("listar_chamados"))
            elif resultado["tipo"] == "admin":
                return redirect(url_for("admin"))
        else:
            flash("Login inválido!")
            return redirect(url_for("login"))

    return render_template("login.html")



# ================ DELETAR CHAMADO ==============
@app.route("/deletar_chamado/<int:id>", methods=["POST"])
def deletar_chamado(id):
    if "usuario" not in session:
        return redirect(url_for("login"))

    conexao = get_db_connection()
    cursor = conexao.cursor()

    # pega o chamado
    cursor.execute("SELECT usuario FROM chamados WHERE id = ?", (id,))
    chamado = cursor.fetchone()

    if not chamado:
        conexao.close()
        return "Chamado não encontrado"

    # 👤 usuário só pode excluir o próprio
    if session["tipo"] == "usuario":
        if chamado["usuario"] != session["usuario"]:
            conexao.close()
            return "Você não pode excluir esse chamado!"

    # 👨‍🔧 técnico/admin pode tudo

    cursor.execute("DELETE FROM chamados WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()

    flash("Chamado excluído com sucesso!")
    return redirect(url_for("listar_chamados"))


# ================= ADMIN =================
@app.route("/admin")
def admin():
    if "usuario" not in session or session["tipo"] != "admin":
        return "Acesso negado!"
    
    return render_template("admin.html")

# ================= LISTAR USUÁRIOS =================
@app.route("/listar_usuarios")
def listar_usuarios():
    if "usuario" not in session or session["tipo"] != "admin":
        return "Acesso negado!"

    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    conexao.close()

    return render_template("listar_usuarios.html", usuarios=usuarios)

# ================= DELETAR USUÁRIO =================
@app.route("/deletar_usuario/<int:id>", methods=["POST"])
def deletar_usuario(id):
    if "usuario" not in session or session["tipo"] != "admin":
        return "Acesso negado!"

    conexao = get_db_connection()
    cursor = conexao.cursor()

    # 👉 pega o usuário que será deletado
    cursor.execute("SELECT login FROM usuarios WHERE id = ?", (id,))
    usuario_alvo = cursor.fetchone()

    if usuario_alvo:
        # 👉 impede deletar a si mesmo
        if session["usuario"] == usuario_alvo["login"]:
            conexao.close()
            return "Você não pode excluir seu próprio usuário!"

    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()

    flash("Usuário removido com sucesso!")
    return redirect(url_for("listar_usuarios"))

# ================= LISTAR CHAMADOS =================
@app.route("/chamados")
def listar_chamados():
    if "usuario" not in session:
        flash("Você precisa estar logado!")
        return redirect(url_for("login"))

    status = request.args.get("status")
    nivel = request.args.get("nivel")
    data = request.args.get("data")
    usuario_filtro = request.args.get("usuario")

    conexao = get_db_connection()
    cursor = conexao.cursor()

    query = "SELECT * FROM chamados WHERE 1=1"
    params = []

    # 🔒 usuário só vê os próprios
    if session["tipo"] == "usuario":
        query += " AND usuario = ?"
        params.append(session["usuario"])

    # 🎯 filtros
    if status:
        query += " AND status = ?"
        params.append(status)

    if nivel:
        query += " AND nivel = ?"
        params.append(nivel)

    if usuario_filtro and session["tipo"] != "usuario":
        query += " AND usuario LIKE ?"
        params.append(f"%{usuario_filtro}%")

    if data:
        query += " AND data LIKE ?"
        params.append(f"%{data}%")

    cursor.execute(query, params)
    chamados = cursor.fetchall()

    conexao.close()

    return render_template("listar_chamados.html", chamados=chamados)


# ================= MEUS CHAMADOS =================
@app.route("/meus_chamados")
def meus_chamados():
    if "usuario" not in session:
        return redirect(url_for("login"))

    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM chamados WHERE usuario = ?",
        (session["usuario"],)
    )

    chamados = cursor.fetchall()
    conexao.close()

    return render_template("meus_chamados.html", chamados=chamados)

# ================= ABRIR CHAMADO =================
@app.route("/abrir_chamado", methods=["GET", "POST"])
def abrir_chamado():
    if "usuario" not in session:
        flash("Você precisa estar logado!")
        return redirect(url_for("login"))

    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        usuario_logado = session["usuario"]
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

        if not titulo or not descricao:
            flash("Preencha todos os campos!")
            return redirect(url_for("abrir_chamado"))

        conexao = get_db_connection()
        cursor = conexao.cursor()

        cursor.execute(
            "INSERT INTO chamados (titulo, descricao, status, usuario, data) VALUES (?, ?, ?, ?, ?)",
            (titulo, descricao, "aberto", usuario_logado, data_atual)
        )

        conexao.commit()
        conexao.close()

        flash("Chamado aberto com sucesso!")
        return redirect(url_for("listar_chamados"))

    return render_template("abrir_chamado.html")

# ================= ATUALIZAR STATUS =================
@app.route("/atualizar_status/<int:id>", methods=["POST"])
def atualizar_status(id):
    if "usuario" not in session or session["tipo"] == "usuario":
        flash("Você não tem permissão!")
        return redirect(url_for("listar_chamados"))

    novo_status = request.form["status"]

    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE chamados SET status = ? WHERE id = ?",
        (novo_status, id)
    )

    conexao.commit()
    conexao.close()

    flash("Status alterado com sucesso!")
    return redirect(url_for("listar_chamados"))

# ================= ATUALIZAR NÍVEL =================
@app.route("/atualizar_nivel/<int:id>", methods=["POST"])
def atualizar_nivel(id):
    if "usuario" not in session or session["tipo"] == "usuario":
        flash("Você não tem permissão!")
        return redirect(url_for("listar_chamados"))

    novo_nivel = request.form["nivel"]

    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE chamados SET nivel = ? WHERE id = ?",
        (novo_nivel, id)
    )

    conexao.commit()
    conexao.close()

    flash("Nível alterado com sucesso!")
    return redirect(url_for("listar_chamados"))

# ================= CRIAR USUÁRIO =================
@app.route("/criar_usuario", methods=["POST"])
def criar_usuario():
    if "usuario" not in session or session["tipo"] != "admin":
        return "Acesso negado!"

    login = request.form["login"]
    senha = request.form["senha"]
    tipo = request.form["tipo"]

    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO usuarios (login, senha, tipo) VALUES (?, ?, ?)",
        (login, senha, tipo)
    )

    conexao.commit()
    conexao.close()

    flash("Usuário criado com sucesso!")
    return redirect(url_for("admin"))

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu do sistema.")
    return redirect(url_for("login"))

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
