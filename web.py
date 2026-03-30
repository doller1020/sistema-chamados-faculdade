from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = "1234"  # obrigatório para sessões

# Função para conectar ao banco
def get_db_connection():
    conn = sqlite3.connect("database.db")
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
            # Salva usuário na sessão
            session["usuario"] = usuario
            session["tipo"] = resultado[0]

            tipo = resultado[0]
            if tipo == "usuario":
                return redirect(url_for("abrir_chamado"))
            elif tipo == "tecnico":
                return redirect(url_for("listar_chamados"))
            elif tipo == "admin":
                return "<h1>Painel Admin (em construção)</h1>"
        else:
            flash("Login inválido!")
            return redirect(url_for("login"))

    return render_template("login.html")

# ================= LISTAR CHAMADOS =================
@app.route("/chamados")
def listar_chamados():
    # Só permite técnicos e admin
    if "usuario" not in session:
        flash("Você precisa estar logado!")
        return redirect(url_for("login"))

    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM chamados")
    chamados = cursor.fetchall()

    conexao.close()
    return render_template("listar_chamados.html", chamados=chamados)

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

        if not titulo or not descricao:
            flash("Preencha todos os campos!")
            return redirect(url_for("abrir_chamado"))

        conexao = get_db_connection()
        cursor = conexao.cursor()

        # Inserir no banco incluindo o usuário
        cursor.execute(
            "INSERT INTO chamados (titulo, descricao, status, usuario) VALUES (?, ?, ?, ?)",
            (titulo, descricao, "Aberto", usuario_logado)
        )

        conexao.commit()
        conexao.close()

        flash("Chamado aberto com sucesso!")
        return redirect(url_for("listar_chamados"))

    return render_template("abrir_chamado.html")

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu do sistema.")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
