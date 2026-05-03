import sqlite3

# Conecta (ou cria) o banco
conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

# ================= USUÁRIOS =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    tipo TEXT NOT NULL
)
""")

# ================= CHAMADOS =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS chamados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    status TEXT NOT NULL,
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
]

for usuario in usuarios:
    try:
        cursor.execute(
            "INSERT INTO usuarios (login, senha, tipo) VALUES (?, ?, ?)",
            usuario
        )
    except sqlite3.IntegrityError:
        pass

conexao.commit()
conexao.close()

print("Banco criado com sucesso!")
print("Login padrão:")
print("admin / 123")
print("wingrid / 1234")
print("tecnico1 / 1234")
print("tecnico2 / 1234")
print("tecnico3 / 1234")
print("gerente / 1234")