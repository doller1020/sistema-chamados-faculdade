import sqlite3

conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

cursor.execute("ALTER TABLE chamados ADD COLUMN status TEXT")

conexao.commit()
conexao.close()

print("Coluna status adicionada!")
