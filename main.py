
import json


def visualizar_json(nome_arquivo):
    try:
        dados = [{}]
        # Retorna os dados contidos no arquivo, caso existente.
        with open(nome_arquivo + ".json", "r") as f:
            if f:
                dados = json.load(f)
                f.close()
                return dados
    except:
        return False


def salvar_json(nome_arquivo, novo_arquivo):
    try:
        # Sobrescreve ou cria um arquivo.
        with open(nome_arquivo + ".json", "w") as f:
            json.dump(novo_arquivo, f, indent=4)
            f.close()
    except:
        print("Erro ao tentar salvar o arquivo.")


def codigo_existe(codigo, nome_arquivo):
    try:
        arquivo = visualizar_json(nome_arquivo)
        # Verifica se o arquivo existe e depois se o código já existe.
        # Se o código existir retorna seus dados, seu índice na lista, e o arquivo para edições posteriores.
        if arquivo:
            for index, cliente in enumerate(arquivo):
                if codigo == cliente["cod"]:
                    return cliente, index, arquivo
        return False
    except ValueError:
        print("Valor informado incorreto.")

def solicitar_dados(nome_submenu):
    while True:
        try:
            chaves = []
            dados = {}
            # Verifica se o código primário é maior que 0 e se ja existe.
            def codigo_primario_valido(codigo, nome_arquivo = nome_submenu):
                if codigo <= 0 or codigo_existe(codigo, nome_arquivo):
                    print("O código informado já existe ou é menor que 1.")
                    return False
                else:
                    return True
            # chaves(keys) padrões de cada submenu.
            if nome_submenu == "disciplina":
                chaves = ["nome"]
            elif nome_submenu == "turma":
                chaves = ["professor", "disciplina"]
            elif nome_submenu == "matricula":
                chaves = ["turma", "estudante"]
            else:
                chaves = ["nome", "cpf"]

            codigo_primario = int(input(f"Informe o código de {nome_submenu}: "))
            # Faz a verificação de código primário e o lança no dicionário temporário.
            if codigo_primario_valido(codigo_primario):
                dados.update({"cod": codigo_primario})
                for chave in chaves:
                    # Verifica se é necessário retornar se o código já existe
                    if nome_submenu == "turma" or nome_submenu == "matricula":
                        dado = int(input(f"Informe o código de {chave}: "))
                        if not codigo_existe(int(dado), str(chave)):
                            print(f"O código de {chave} não existe.")
                            return False
                    else:
                        dado = input(f"Informe o {chave}: ")
                    # Lança o restante dos dados no dicionário temporário.
                    dados.update({f"{chave}": dado})
                return dados
                break
            else:
                continue
        # É feita uma exceção para erro de valor.
        except ValueError:
            print("Valor informado incorreto.")


def listar_cliente(nome_arquivo):
    try:
        lista = visualizar_json(nome_arquivo)
        chaves = []
        if nome_arquivo == "turma":
            chaves = ["professor", "disciplina"]
        elif nome_arquivo == "matricula":
            chaves = ["turma", "estudante"]
        # Verifica se o arquivo existe e retorna os dados
        if not lista:
            print("Não há dados cadastrados.\n")
        elif lista and nome_arquivo == "turma" or lista and nome_arquivo == "matricula":
            print(f"Listagem do menu {nome_arquivo}: \n")

            for item in lista:
                dados = {}
                print(f"Dados de {nome_arquivo} de código >{item['cod']}<: ")
                for chave in chaves:
                    cliente = codigo_existe(int(item[chave]), str(chave))
                    # Se o código existe, então são mostrados seus dados.
                    if cliente:
                        dados_cliente, index, arquivo = codigo_existe(int(item[chave]), str(chave))
                        print(f"    {chave} (código: {dados_cliente['cod']}):")
                        dados_cliente.pop("cod")
                        print(f"        {dados_cliente}")
                        for chave_secundaria in dados_cliente:
                            # Se há uma chave(key) dentro dos dados principais, são feitas buscas para recuperar e mostrar os dados secundários. Cruzamento de informações.
                            if chave_secundaria == "professor" or chave_secundaria == "disciplina" or chave_secundaria == "turma" or chave_secundaria == "estudante":
                                cliente_secundario = codigo_existe(int(dados_cliente[chave_secundaria]), str(chave_secundaria))
                                if cliente_secundario:
                                    dados_secundarios, index_secundario, arquivo_secundario = codigo_existe(int(dados_cliente[chave_secundaria]), str(chave_secundaria))
                                    dados_secundarios.pop("cod")
                                    print(f"            {chave_secundaria} {dados_cliente[chave_secundaria]}:")
                                    print(f"                {dados_secundarios}:")
                    else:
                        print(f"    {chave}:")
                        print(f"        inexistente.")
                print("\n")
        else:
            print(f"Listagem do menu {nome_arquivo}: \n")
            for item in lista:
                print(f" - {item}")
            print("\n")
    except:
        print("Erro ao listar dados.")


def excluir_cliente(nome_arquivo):
    while True:
        try:
            lista = visualizar_json(nome_arquivo)
            # Verifica se o arquivo existe antes de proceder.
            if lista:
                codigo = int(input("Informe o codigo do cliente que deseja excluir (0 para voltar): "))
                if codigo == 0:
                    break

                cliente_existe = codigo_existe(codigo, nome_arquivo)
                # Se o código existe, procede com a exclusão.
                if cliente_existe == False:
                    print("\nO código informado para exclusão não existe.\n")
                    continue
                elif codigo and cliente_existe:
                    print("Excluindo...\n")
                    cliente, index, arquivo = codigo_existe(codigo, nome_arquivo)
                    arquivo.pop(index)
                    salvar_json(nome_arquivo, arquivo)
                    print("Sucesso!")

                if input("\nDeseja excluir outro cadastro?(s/n): \n") == "s":
                    continue
                else:
                    break
            else:
                print("Não há dados cadastrados.\n")
                break
        # É feita uma exceção para erro de valor.
        except ValueError:
            print("Tipo de valor inválido!")


def editar_cliente(nome_arquivo):
    while True:
        try:
            lista = visualizar_json(nome_arquivo)
            # Verifica se o arquivo existe antes de proceder.
            if lista:
                codigo = int(input(f"Informe o código de {nome_arquivo} que deseja editar (0 para voltar): "))
                if codigo == 0:
                    break
                elif codigo_existe(codigo, nome_arquivo) == False:
                    print("O código informado para alteração não existe.")
                    continue
                else:
                    # Se o código existe, são solicitados os dados e procede com as alterações.
                    novos_dados = solicitar_dados(nome_arquivo)
                    if not novos_dados:
                        continue
                    if codigo_existe(novos_dados["cod"], nome_arquivo):
                        print("\nO novo código informado já existe.\n")
                        continue
                    else:
                        cliente, index, novo_arquivo = codigo_existe(codigo, nome_arquivo)
                        print("Editando...\n")
                        for chave in cliente.keys():
                            cliente[str(chave)] = novos_dados[str(chave)]
                            salvar_json(nome_arquivo, novo_arquivo)
                        print("Sucesso!")

                        if input("\nDeseja continuar editando?(s/n): \n") == "s":
                            continue
                        else:
                            break
            else:
                print("Não há dados cadastrados.\n")
                break
        # É feita uma exceção para erro de valor.
        except ValueError:
            print("Tipo de valor inválido!")


def incluir_cliente(nome_arquivo):
    while True:
        try:
            arquivo = visualizar_json(nome_arquivo)
            novos_dados = solicitar_dados(nome_arquivo)
            novo_arquivo = arquivo
            # Verifica se há novos dados e verifica se o código existe.
            if novos_dados:
                cliente = codigo_existe(novos_dados["cod"], nome_arquivo)
            else:
                continue
            # Se o arquivo existe e o cliente não, os novos dados são incluídos no arquivo.
            if arquivo and cliente == False:
                novo_arquivo = arquivo + [novos_dados]
            # Se o arquivo e cliente existem, o usuário deve informar um código não utilizado para proceder.
            elif arquivo and cliente:
                print("\nO código já existe.\n")
                continue
            # Se o arquivo e cliente não existem, é criado um arquivo com os dados informados.
            else:
                novo_arquivo = [novos_dados]

            print("\nIncluindo...\n")
            salvar_json(nome_arquivo, novo_arquivo)
            print("Sucesso!")

            if input("\nDeseja continuar cadastrando?(s/n): \n") == "s":
                continue
            else:
                break
        # É feita uma exceção para erro de valor.
        except ValueError:
            print("Tipo de valor inválido!")


def acessar_menu_acao(submenu_nome):
    while True:
        try:
            acao_lista = ["Incluir", "Listar", "Editar", "Excluir", "Voltar ao menu principal"]

            # Através do laço for são mostradas as ações e devidas númerações começando por 1 (índice + 1).
            print(f"Qual ação deseja realizar no menu {submenu_nome}?")
            for i, acao in enumerate(acao_lista):
                print(f"({i + 1}){acao}")
            acao = int(input())

            # Verifica se o número de ação selecionado é igual ou menor a 0, ou maior que o tamanho da lista de ações.
            if acao <= 0 or acao > len(acao_lista):
                print("\nSelecione uma ação válida!\n")
                continue
            # Verifica se a opção selecionada está entre as desabilitadas.
            # Voltar ao menu principal é a última opção da lista, portanto excetuada (tamanho da lista - 1).
            elif 5 <= acao <= len(acao_lista) - 1:
                print("\nEm desenvolvimento!\nRetornando ao menu de ações...\n")
                continue
            # Volta ao menu principal selecionando a opção 5.
            elif acao == 5:
                print("\nVoltando ao menu principal...\n")
                acessar_menu_principal()
                break
            # Define o nome da ação a ser printada através do índice (índice - 1).
            else:
                acao_nome = acao_lista[acao - 1]

            print(f"\nVocê selecionou a opção {acao_nome} do menu {submenu_nome}\n")
            if acao == 1:
                incluir_cliente(submenu_nome.lower())
            elif acao == 2:
                listar_cliente(submenu_nome.lower())
            elif acao == 3:
                editar_cliente(submenu_nome.lower())
            elif acao == 4:
                excluir_cliente(submenu_nome.lower())

    # É feita uma exceção para erro de valor.
        except ValueError:
            print("Tipo de valor inválido!")


def acessar_menu_principal():
    while True:
        try:
            opcao_lista = ["Estudante", "Professor", "Disciplina", "Turma", "Matricula", "Sair do menu principal"]

            # Através do laço for são mostradas as opções e devidas númerações começando por 1 (índice + 1).
            print("Qual submenu deseja acessar?")
            for i, opcao in enumerate(opcao_lista):
                print(f"({i + 1}){opcao}")
            opcao_submenu = int(input())

            # Verifica se o número de ação selecionado é igual ou menor a 0, ou maior que o tamanho da lista de opções.
            if opcao_submenu <= 0 or opcao_submenu > len(opcao_lista):
                print("\nSelecione um submenu válido!\n")
                continue
            # Encerra o menu principal selecionando a opção 6.
            if opcao_submenu == 6:
                exit("Menu principal encerrado.")

            # Passa como parâmetro da função acessar_menu_acao() e printa para o usuário o nome da opção selecionada,
            # através do índice (numero do input - 1).
            print(f"\nAcessando o menu {opcao_lista[opcao_submenu -1]}...\n")
            acessar_menu_acao(opcao_lista[opcao_submenu - 1])
            break

        # É feita uma exceção para erro de valor.
        except ValueError:
            print("Tipo de valor inválido!")


# Inicia o programa.
acessar_menu_principal()
