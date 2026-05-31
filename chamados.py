import sqlite3

def abrir_chamado(usuario):
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    print("\n=== ABRIR CHAMADO ===")
    titulo = input("Título: ")
    descricao = input("Descrição: ")

    cursor.execute(
    "INSERT INTO chamados (titulo, descricao, status, usuario) VALUES (?, ?, ?, ?)",
    (titulo, descricao, "aberto", session["usuario"])
)
    conexao.commit()
    conexao.close()

    print("Chamado aberto com sucesso!")
    
def listar_chamados():
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT id, titulo, status, usuario FROM chamados")
    chamados = cursor.fetchall()

    print("\n=== LISTA DE CHAMADOS ===")

    for chamado in chamados:
        print(f"ID: {chamado[0]}")
        print(f"Título: {chamado[1]}")
        print(f"Status: {chamado[2]}")
        print(f"Usuário: {chamado[3]}")
        print("------------------------")

    conexao.close()
def atualizar_status():
    import sqlite3

    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    print("\n=== ATUALIZAR STATUS DO CHAMADO ===")

    id_chamado = input("Digite o ID do chamado: ")

    print("1 - Em atendimento")
    print("2 - Resolvido")

    opcao = input("Escolha o novo status: ")

    if opcao == "1":
        status = "em atendimento"
    elif opcao == "2":
        status = "resolvido"
    else:
        print("Opção inválida!")
        return

    cursor.execute(
        "UPDATE chamados SET status = ? WHERE id = ?",
        (status, id_chamado)
    )

    conexao.commit()
    conexao.close()

    print("Status atualizado com sucesso!")
