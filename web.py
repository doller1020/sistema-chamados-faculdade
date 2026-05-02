from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "1234"

<<<<<<< HEAD
=======

>>>>>>> 08da14c (Atualização completa sistema chamados)
# ================= CONEXÃO =================
def get_db_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "database.db")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

<<<<<<< HEAD
# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
=======

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():

>>>>>>> 08da14c (Atualização completa sistema chamados)
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        conexao = get_db_connection()
        cursor = conexao.cursor()

        cursor.execute(
<<<<<<< HEAD
            "SELECT tipo FROM usuarios WHERE login = ? AND senha = ?",
            (usuario, senha)
        )
=======
            "SELECT * FROM usuarios WHERE login=? AND senha=?",
            (usuario, senha)
        )

>>>>>>> 08da14c (Atualização completa sistema chamados)
        resultado = cursor.fetchone()
        conexao.close()

        if resultado:
<<<<<<< HEAD
            session["usuario"] = usuario
=======
            session["usuario"] = resultado["login"]
>>>>>>> 08da14c (Atualização completa sistema chamados)
            session["tipo"] = resultado["tipo"]

            if resultado["tipo"] == "usuario":
                return redirect(url_for("abrir_chamado"))
<<<<<<< HEAD
            elif resultado["tipo"] == "tecnico":
                return redirect(url_for("listar_chamados"))
            elif resultado["tipo"] == "admin":
                return redirect(url_for("admin"))
        else:
            flash("Login inválido!")
            return redirect(url_for("login"))
=======

            elif resultado["tipo"] in ["tecnico_n1", "tecnico_n2", "tecnico_n3"]:
                return redirect(url_for("listar_chamados"))

            elif resultado["tipo"] == "admin":
                return redirect(url_for("admin"))

            elif resultado["tipo"] == "gerente":
                return redirect(url_for("gerente"))

        flash("Login inválido!")
        return redirect(url_for("login"))
>>>>>>> 08da14c (Atualização completa sistema chamados)

    return render_template("login.html")


<<<<<<< HEAD

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
=======
# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
>>>>>>> 08da14c (Atualização completa sistema chamados)


# ================= ADMIN =================
@app.route("/admin")
def admin():
    if "usuario" not in session or session["tipo"] != "admin":
<<<<<<< HEAD
        return "Acesso negado!"
    
    return render_template("admin.html")

# ================= LISTAR USUÁRIOS =================
@app.route("/listar_usuarios")
def listar_usuarios():
    if "usuario" not in session or session["tipo"] != "admin":
        return "Acesso negado!"
=======
        return "Acesso negado"

    return render_template("admin.html")


# ================= GERENTE =================
@app.route("/gerente")
def gerente():
    if "usuario" not in session or session["tipo"] != "gerente":
        return "Acesso negado"
>>>>>>> 08da14c (Atualização completa sistema chamados)

    conexao = get_db_connection()
    cursor = conexao.cursor()

<<<<<<< HEAD
    cursor.execute("SELECT * FROM usuarios")
=======
    cursor.execute("""
        SELECT * FROM chamados
        WHERE status='finalizado'
        ORDER BY id DESC
    """)

    chamados = cursor.fetchall()
    conexao.close()

    return render_template("gerente.html", chamados=chamados)


# ================= USUÁRIOS ADMIN =================
@app.route("/usuarios")
def usuarios():

    if "usuario" not in session or session["tipo"] != "admin":
        return "Acesso negado"

    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM usuarios ORDER BY id ASC")
>>>>>>> 08da14c (Atualização completa sistema chamados)
    usuarios = cursor.fetchall()

    conexao.close()

<<<<<<< HEAD
    return render_template("listar_usuarios.html", usuarios=usuarios)

# ================= DELETAR USUÁRIO =================
@app.route("/deletar_usuario/<int:id>", methods=["POST"])
def deletar_usuario(id):
    if "usuario" not in session or session["tipo"] != "admin":
        return "Acesso negado!"
=======
    return render_template("usuarios.html", usuarios=usuarios)


# ================= EXCLUIR USUÁRIO =================
@app.route("/excluir_usuario/<int:id>")
def excluir_usuario(id):

    if "usuario" not in session or session["tipo"] != "admin":
        return "Acesso negado"
>>>>>>> 08da14c (Atualização completa sistema chamados)

    conexao = get_db_connection()
    cursor = conexao.cursor()

<<<<<<< HEAD
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
=======
    cursor.execute("DELETE FROM usuarios WHERE id=?", (id,))
    conexao.commit()
    conexao.close()

    return redirect(url_for("usuarios"))


# ================= EDITAR USUÁRIO =================
@app.route("/editar_usuario/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):

    if "usuario" not in session or session["tipo"] != "admin":
        return "Acesso negado"
>>>>>>> 08da14c (Atualização completa sistema chamados)

    conexao = get_db_connection()
    cursor = conexao.cursor()

<<<<<<< HEAD
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
=======
    if request.method == "POST":

        login = request.form["login"]
        senha = request.form["senha"]
        tipo = request.form["tipo"]

        cursor.execute("""
            UPDATE usuarios
            SET login=?, senha=?, tipo=?
            WHERE id=?
        """, (login, senha, tipo, id))
>>>>>>> 08da14c (Atualização completa sistema chamados)

        conexao.commit()
        conexao.close()

<<<<<<< HEAD
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
=======
        return redirect(url_for("usuarios"))

    cursor.execute("SELECT * FROM usuarios WHERE id=?", (id,))
    usuario = cursor.fetchone()

    conexao.close()

    return render_template("editar_usuario.html", usuario=usuario)

>>>>>>> 08da14c (Atualização completa sistema chamados)

# ================= CRIAR USUÁRIO =================
@app.route("/criar_usuario", methods=["POST"])
def criar_usuario():
<<<<<<< HEAD
    if "usuario" not in session or session["tipo"] != "admin":
        return "Acesso negado!"
=======

    if "usuario" not in session or session["tipo"] != "admin":
        return "Acesso negado"
>>>>>>> 08da14c (Atualização completa sistema chamados)

    login = request.form["login"]
    senha = request.form["senha"]
    tipo = request.form["tipo"]

    conexao = get_db_connection()
    cursor = conexao.cursor()

<<<<<<< HEAD
    cursor.execute(
        "INSERT INTO usuarios (login, senha, tipo) VALUES (?, ?, ?)",
        (login, senha, tipo)
    )
=======
    cursor.execute("""
        INSERT INTO usuarios (login, senha, tipo)
        VALUES (?, ?, ?)
    """, (login, senha, tipo))
>>>>>>> 08da14c (Atualização completa sistema chamados)

    conexao.commit()
    conexao.close()

    flash("Usuário criado com sucesso!")
    return redirect(url_for("admin"))

<<<<<<< HEAD
# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu do sistema.")
    return redirect(url_for("login"))

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
=======

# ================= ABRIR CHAMADO =================
@app.route("/abrir_chamado", methods=["GET", "POST"])
def abrir_chamado():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        usuario_logado = session["usuario"]
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

        conexao = get_db_connection()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO chamados
            (titulo, descricao, status, usuario, nivel, data_abertura)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            titulo,
            descricao,
            "aberto",
            usuario_logado,
            "N1",
            data_atual
        ))

        conexao.commit()
        conexao.close()

        return render_template(
            "mensagem.html",
            titulo="Chamado aberto com sucesso!",
            mensagem="Seu chamado foi registrado no sistema."
        )

    return render_template("abrir_chamado.html")


# ================= MEUS CHAMADOS =================
@app.route("/meus_chamados")
def meus_chamados():

    if "usuario" not in session:
        return redirect(url_for("login"))

    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM chamados
        WHERE usuario=?
        ORDER BY id DESC
    """, (session["usuario"],))

    chamados = cursor.fetchall()
    conexao.close()

    return render_template("meus_chamados.html", chamados=chamados)


# ================= LISTAR CHAMADOS =================
@app.route("/chamados")
def listar_chamados():

    if "usuario" not in session:
        return redirect(url_for("login"))

    tipo = session["tipo"]

    if tipo == "tecnico_n1":
        nivel = "N1"
    elif tipo == "tecnico_n2":
        nivel = "N2"
    elif tipo == "tecnico_n3":
        nivel = "N3"
    else:
        return "Acesso negado"

    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM chamados
        WHERE nivel=?
        AND status!='finalizado'
        AND (bloqueado_por IS NULL OR bloqueado_por=?)
        ORDER BY id ASC
    """, (nivel, session["usuario"]))

    chamados = cursor.fetchall()
    conexao.close()

    return render_template("listar_chamados.html", chamados=chamados)


# ================= RESOLVER =================
@app.route("/resolver/<int:id>")
def resolver(id):

    if "usuario" not in session:
        return redirect(url_for("login"))

    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE chamados
        SET bloqueado_por=?,
            status='em andamento',
            tecnico_responsavel=?,
            data_atendimento=?
        WHERE id=?
    """, (
        session["usuario"],
        session["usuario"],
        datetime.now().strftime("%d/%m/%Y %H:%M"),
        id
    ))

    conexao.commit()

    cursor.execute("SELECT * FROM chamados WHERE id=?", (id,))
    chamado = cursor.fetchone()

    conexao.close()

    return render_template("painel_resolver.html", chamado=chamado)


# ================= FINALIZAR =================
@app.route("/finalizar/<int:id>", methods=["POST"])
def finalizar(id):

    resposta = request.form["resposta"]

    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE chamados
        SET status='finalizado',
            resposta_tecnica=?,
            data_finalizacao=?
        WHERE id=?
    """, (
        resposta,
        datetime.now().strftime("%d/%m/%Y %H:%M"),
        id
    ))

    conexao.commit()
    conexao.close()

    return redirect(url_for("listar_chamados"))


# ================= ENCAMINHAR =================
@app.route("/encaminhar/<int:id>", methods=["POST"])
def encaminhar(id):

    tipo = session["tipo"]

    if tipo == "tecnico_n1":
        novo = "N2"
    elif tipo == "tecnico_n2":
        novo = "N3"
    else:
        novo = "N3"

    resposta = request.form["resposta"]

    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE chamados
        SET nivel=?,
            status='aberto',
            resposta_tecnica=?,
            bloqueado_por=NULL
        WHERE id=?
    """, (novo, resposta, id))

    conexao.commit()
    conexao.close()

    return redirect(url_for("listar_chamados"))


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 08da14c (Atualização completa sistema chamados)
