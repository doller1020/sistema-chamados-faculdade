print("Sistema de Chamados - Projeto Acadêmico iniciado")

print("================================")
print(" Sistema de Chamados - Faculdade")
print("================================")

print("1 - Abrir chamado")
print("2 - Sair")

opcao = input("Escolha uma opção: ")

if opcao == "1":
    descricao = input("Descreva o problema: ")
    print("Chamado aberto com sucesso!")
    print("Descrição:", descricao)

elif opcao == "2":
    print("Encerrando o sistema...")

else:
    print("Opção inválida")

