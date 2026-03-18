import sqlite3

# Conecta (ou cria) o banco de dados
conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

# Criação da tabela de usuários
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    tipo TEXT NOT NULL
)
""")
# Criação da tabela de chamados
cursor.execute("""
CREATE TABLE IF NOT EXISTS chamados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    status TEXT NOT NULL,
    usuario TEXT NOT NULL
)
""")

# Inserção de usuários padrão
usuarios = [
    ("admin", "admin123", "administrador"),
    ("wingrid", "1234", "usuario"),
    ("doller", "1234", "tecnico")
]

for usuario in usuarios:
    try:
        cursor.execute(
            "INSERT INTO usuarios (login, senha, tipo) VALUES (?, ?, ?)",
            usuario
        )
    except sqlite3.IntegrityError:
        pass  # evita erro se o usuário já existir

# Salva e fecha
conexao.commit()
conexao.close()

print("Banco de dados criado com sucesso!")
print("Usuários cadastrados: administrador, usuário e técnico.")

