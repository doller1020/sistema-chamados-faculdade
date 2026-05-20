import sqlite3

conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

try:
    cursor.execute("""
    ALTER TABLE chamados
    ADD COLUMN bloqueado_por TEXT
    """)
except:
    print("Coluna bloqueado_por já existe")

try:
    cursor.execute("""
    ALTER TABLE chamados
    ADD COLUMN tecnico_responsavel TEXT
    """)
except:
    print("Coluna tecnico_responsavel já existe")

try:
    cursor.execute("""
    ALTER TABLE chamados
    ADD COLUMN resposta_tecnica TEXT
    """)
except:
    print("Coluna resposta_tecnica já existe")

try:
    cursor.execute("""
    ALTER TABLE chamados
    ADD COLUMN data_abertura TEXT
    """)
except:
    print("Coluna data_abertura já existe")

try:
    cursor.execute("""
    ALTER TABLE chamados
    ADD COLUMN data_atendimento TEXT
    """)
except:
    print("Coluna data_atendimento já existe")

try:
    cursor.execute("""
    ALTER TABLE chamados
    ADD COLUMN data_finalizacao TEXT
    """)
except:
    print("Coluna data_finalizacao já existe")

conexao.commit()
conexao.close()

print("Banco atualizado com sucesso!")