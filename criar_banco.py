import sqlite3
<<<<<<< HEAD

# Conecta (ou cria) o banco de dados
conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

# Criação da tabela de usuários
=======
# Conecta ou cria banco
conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

# ================= USUÁRIOS =================
>>>>>>> 08da14c (Atualização completa sistema chamados)
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    tipo TEXT NOT NULL
)
""")
<<<<<<< HEAD
# Criação da tabela de chamados
=======

# ================= CHAMADOS =================
>>>>>>> 08da14c (Atualização completa sistema chamados)
cursor.execute("""
CREATE TABLE IF NOT EXISTS chamados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    status TEXT NOT NULL,
<<<<<<< HEAD
    usuario TEXT NOT NULL
)
""")

# Inserção de usuários padrão
usuarios = [
    ("admin", "admin123", "administrador"),
    ("wingrid", "1234", "usuario"),
    ("doller", "1234", "tecnico")
=======
    usuario TEXT NOT NULL,
    nivel TEXT,
    tecnico_responsavel TEXT,
    resposta_tecnica TEXT,
    data_abertura TEXT,
    data_atendimento TEXT,
    data_finalizacao TEXT,
    bloqueado_por TEXT
)
""")

# ================= USUÁRIOS PADRÃO =================
usuarios = [
    ("admin", "123", "admin"),
    ("wingrid", "1234", "usuario"),
    ("tecnico1", "1234", "tecnico_n1"),
    ("tecnico2", "1234", "tecnico_n2"),
    ("tecnico3", "1234", "tecnico_n3"),
    ("gerente", "1234", "gerente")
>>>>>>> 08da14c (Atualização completa sistema chamados)
]

for usuario in usuarios:
    try:
        cursor.execute(
            "INSERT INTO usuarios (login, senha, tipo) VALUES (?, ?, ?)",
            usuario
        )
    except sqlite3.IntegrityError:
<<<<<<< HEAD
        pass  # evita erro se o usuário já existir

# Salva e fecha
conexao.commit()
conexao.close()

print("Banco de dados criado com sucesso!")
print("Usuários cadastrados: administrador, usuário e técnico.")

=======
        pass

# Salvar
conexao.commit()
conexao.close()

print("Banco criado com sucesso!")
print("Perfis criados:")
print("admin / 123")
print("wingrid / 1234")
print("tecnico1 / 1234")
print("tecnico2 / 1234")
print("tecnico3 / 1234")
print("gerente / 1234")
>>>>>>> 08da14c (Atualização completa sistema chamados)
