from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        conexao = sqlite3.connect("database.db")
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT tipo FROM usuarios WHERE login = ? AND senha = ?",
            (usuario, senha)
        )

        resultado = cursor.fetchone()
        conexao.close()

        if resultado:
            tipo = resultado[0]

            if tipo == "usuario":
                return render_template("usuario.html")
            elif tipo == "tecnico":
                return render_template("tecnico.html")
            elif tipo == "admin":
                return render_template("admin.html")
        else:
            return "<h1>Login inválido!</h1>"

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
