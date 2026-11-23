import getpass
import json

print("Seja bem-vindo ao nosso site!")

dados = {
    "usuarios": {},
    "doacoes": []
}

limite_erros = 5


# FUNÇÃO PARA LER OS DADOS
def ler_dados():
    global dados

    try:
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if not isinstance(dados, dict):
            dados = {}

    except FileNotFoundError:
        dados = {}

    except (json.JSONDecodeError, OSError) as erro:
        print("Algo deu errado ao ler o arquivo:", erro)
        dados = {}

    dados.setdefault("usuarios", {})
    dados.setdefault("doacoes", [])


# FUNÇÃO PARA SALVAR OS DADOS
def armazenar_dados():
    try:
        with open("dados.json", "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    except OSError as erro:
        print("Erro ao salvar os dados:", erro)
    


# FUNÇÃO DE CADASTRO
def cadastro_usuario():
    while True:
        usuario = input("Cadastre seu usuário: ").strip()

        if not usuario.isalpha():
            print("O usuário deve conter apenas letras!")
            continue

        if usuario in dados["usuarios"]:
            print("Usuário já existente!")
            continue

        print("Usuário válido!")
        break

    cidade = input("Digite sua cidade: ").strip()
    senha = getpass.getpass("Cadastre sua senha: ")

    dados["usuarios"][usuario] = {
        "cidade": cidade,
        "senha": senha
    }

    armazenar_dados()
    print("Cadastro realizado com sucesso!")


# FUNÇÃO DE LOGIN
def usuario_login():
    tentativas = 0

    while tentativas < limite_erros:
        usuario = input("Digite seu usuário: ").strip()
        senha = getpass.getpass("Digite sua senha: ")

        if usuario in dados["usuarios"]:

            if dados["usuarios"][usuario]["senha"] == senha:
                print("Login realizado com sucesso!")
                print("Bem-vindo,", usuario)
                return usuario

        tentativas += 1

        print("Usuário ou senha incorretos!")
        print("Tentativas restantes:", limite_erros - tentativas)

    print("Limite de tentativas atingido!")
    return None


# FUNÇÃO PARA REALIZAR DOAÇÕES
def realizar_doacao(usuario):
    try:
        valor = float(input("Digite o valor da doação: R$ ").replace(",", "."))

        if valor <= 0:
            print("O valor deve ser maior que zero!")
            return

        doacao = {
            "usuario": usuario,
            "valor": valor
        }

        dados["doacoes"].append(doacao)

        armazenar_dados()

        print("Doação realizada com sucesso!")

    except ValueError:
        print("Digite um valor válido!")


# FUNÇÃO PARA CONSULTAR DOAÇÕES
def consultar_doacoes(usuario):
    print("\n===== SUAS DOAÇÕES =====")

    encontrou = False

    for doacao in dados["doacoes"]:
        if doacao["usuario"] == usuario:
            print("Valor: R$", doacao["valor"])
            encontrou = True

    if not encontrou:
        print("Você ainda não realizou doações.")


# MENU DO USUÁRIO LOGADO
def menu_usuario(usuario):
    while True:
        print("\n===== ÁREA DO USUÁRIO =====")
        print("1 - Realizar doação")
        print("2 - Consultar doações")
        print("3 - Sair da conta")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            realizar_doacao(usuario)

        elif opcao == "2":
            consultar_doacoes(usuario)

        elif opcao == "3":
            print("Saindo da conta...")
            break

        else:
            print("Opção inválida!")


# MENU PRINCIPAL
def menu():
    ler_dados()

    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1 - Cadastrar usuário")
        print("2 - Fazer login")
        print("3 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastro_usuario()

        elif opcao == "2":
            usuario = usuario_login()

            if usuario is not None:
                menu_usuario(usuario)

        elif opcao == "3":
            print("Obrigado por utilizar nosso site!")
            break

        else:
            print("Opção inválida!")


menu()