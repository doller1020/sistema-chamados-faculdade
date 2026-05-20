from flask import session
from chamados import atualizar_status
from chamados import listar_chamados
from chamados import abrir_chamado
import sqlite3

def login():
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    print("=== LOGIN DO SISTEMA ===")
    usuario = input("Login: ")
    senha = input("Senha: ")

    cursor.execute(
        "SELECT login, tipo FROM usuarios WHERE login = ? AND senha = ?",
        (usuario, senha)
    )

    resultado = cursor.fetchone()
    conexao.close()

    if resultado:
        print("\nLogin realizado com sucesso!")
        print(f"Usuário: {resultado[0]}")
        print(f"Perfil: {resultado[1]}")
        return resultado[1]
    else:
        print("\nLogin inválido!")
        return None


# MENUS POR PERFIL

def menu_admin():
    print("\n=== MENU ADMINISTRADOR ===")
    print("1 - Ver usuários")
    print("2 - Ver chamados")
    print("0 - Sair")

def menu_usuario(usuario):
    while True:
        print("\n=== MENU USUÁRIO ===")
        print("1 - Abrir chamado")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            abrir_chamado(usuario)
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def menu_tecnico():
    while True:
        print("\n=== MENU TÉCNICO ===")
        print("1 - Ver chamados")
        print("2 - Atualizar status")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            listar_chamados()
        elif opcao == "2":
            atualizar_status()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


# EXECUÇÃO

perfil = login()

if perfil == "administrador":
    menu_admin()
elif perfil == "usuario":
    menu_usuario(input("Confirme seu login novamente: "))
elif perfil == "tecnico":
    menu_tecnico()
else:
    print("Encerrando sistema...")
