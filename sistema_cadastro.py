# Sistema de Cadastro em Python
# Projeto para prática de lógica, listas, dicionários e funções

# Bibliotecas
from time import sleep

# Funções
def print_grupo_bonito(grupo):
    # Imprime os cadastros formatando apenas a exibição (não altera os dados)
    print('DADOS'.ljust(15), 'VALORES')
    print('-' * 30)

    for pessoa in grupo:
        for k, v in pessoa.items():
            valor = v
            if k == 'telefone':
                valor = formatar_telefone(v)
            if k in ('nome', 'cidade'):
                valor = str(v).title()
            if k == 'estado':
                valor = str(v).upper()

            print(f'{k.ljust(15).capitalize()} {valor}')
        print('=-' * 30)

def formatar_telefone(numero):
    if len(numero) == 11:
        return f'({numero[:2]}) {numero[2:7]}-{numero[7:]}'
    elif len(numero) == 10:
        return f'({numero[:2]}) {numero[2:6]}-{numero[6:]}'
    else:
        return numero  # fallback

def pesquisar(grupo, chave, mensagem):
    # Realiza busca textual (parcial), ideal para strings como nome e cidade
    termo = input(mensagem).strip().lower()
    encontrado = False
    sleep(1)

    for pessoa in grupo:
        valor = str(pessoa[chave]).lower()
        if termo in valor:
            for k, v in pessoa.items():
                print(f'{k}: {v}, ', end='')
            encontrado = True

    if not encontrado:
        print(f'{chave.capitalize()} não encontrado.')
    
    print()

def id_existe(grupo, id_digitado):
    # Verifica se um ID já está cadastrado no sistema
    for pessoa in grupo:
        if pessoa['id'] == id_digitado:
            return True
    return False

def buscar_pessoa_por_id(grupo, id_busca):
    for pessoa in grupo:
        if pessoa['id'] == id_busca:
            return pessoa
    return None


# Programa Principal
grupo = list()
pessoa = dict()
from datetime import datetime, date

print('=-' * 30)
print(' SISTEMA DE CADASTROS '.center(60))
print('=-' * 30)

boas_vindas = "Seja bem-vindo ao sistema de cadastramento!"
for c in boas_vindas:
    print(c, end='')
    sleep(0.06)
print()

# Armazenamento de dados digitados pelo usuário
while True:
    pessoa.clear()
    while True:
        try:
            id_digitado = int(input('\nID numérico: '))
            if id_existe(grupo, id_digitado):
                print('ERRO! Esse ID já está em uso.')
            else:
                pessoa['id'] = id_digitado
                break
        except ValueError:
            print('ID inválido. Digite apenas números.')

    pessoa['nome'] = str(input('Nome completo: ')).title()

    while True:
        try:
            data_str = input('Data de nascimento (DD/MM/AAAA): ').strip()
            data_nascimento = datetime.strptime(data_str, '%d/%m/%Y').date()
            hoje = date.today()

            # Valida se a data não é no futuro
            if data_nascimento > hoje:
                print('A data de nascimento não pode ser no futuro.')
                continue
            break
        except ValueError:
            print('Data inválida. Use o formato DD/MM/AAAA.')

    # Cálculo da idade
    idade = hoje.year - data_nascimento.year
    if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1


    pessoa['nascimento'] = data_nascimento.strftime('%d/%m/%Y')
    pessoa['idade'] = idade
    
    while True:
        sexo = input('Sexo: [M/F] ').strip().upper()
        if sexo and sexo[0] in 'MF':
            pessoa['sexo'] = sexo[0]
            break
        print('ERRO! Digite M ou F.')
    
    while True:
        pessoa['email'] = str(input('Email: ')).strip()
        if '@' in pessoa['email'] and '.' in pessoa['email']:
            break
        print('Email inválido. Tente novamente...')
    
    while True:
        telefone = input('Telefone (somente números): ').strip()
        if telefone.isdigit() and len(telefone) in (10, 11):
            pessoa['telefone'] = telefone
            break
        print('Número inválido! Tente novamente...')
    
    pessoa['cidade'] = str(input('Cidade: '))
    pessoa['estado'] = str(input('Estado (UF): '))
    grupo.append(pessoa.copy())

    while True:
        resp = str(input('Deseja continuar? [S/N] ')).upper()[0]
        if resp in 'SN':
            break
        print('opção inválida! Digite S ou N...')
    if resp == 'N':
        break

    print('-' * 30)

print('=-' * 30)
sleep(1)
print_grupo_bonito(grupo)
sleep(3)

# Opções para o usuário decidir o que fazer com as informações coletadas acima
while True:
    print('''
O que deseja fazer?
[0] Listar todos os cadastros
[1] Pesquisar nome
[2] Filtrar por ID
[3] Filtrar por idade
[4] Filtrar por cidade
[5] Filtrar por estado (UF)
[6] Filtrar por email
[7] Editar cadastro
[8] Excluir cadastro
[9] Sair''')
    while True:
        escolha = input('Escolha uma opção: ')
        if escolha in '0123456789':
            break
        print('ERRO! Digite uma opção válida...')

    if escolha == '0':
        sleep(1)
        print_grupo_bonito(grupo)

    elif escolha == '1':
        pesquisar(grupo, 'nome', 'Digite o nome desejado: ')

    elif escolha == '2':
        pesquisar(grupo, 'id', 'Digite o ID numérico: ')

    elif escolha == '3':
        pesquisar(grupo, 'idade', 'Digite a idade: ')

    elif escolha == '4':
        pesquisar(grupo, 'cidade', 'Digite a cidade: ')
    
    elif escolha == '5':
        pesquisar(grupo, 'estado', 'Digite o estado (UF): ')
    
    elif escolha == '6':
        pesquisar(grupo, 'email', 'Digite o email: ')
    
    elif escolha == '7':
        sleep(0.5)
        try:
            id_editar = int(input('Digite o ID do usuário para editar: '))
        except ValueError:
            print('ID inválido.')
            continue

        pessoa = buscar_pessoa_por_id(grupo, id_editar)

        if pessoa is None:
            print('Usuário não encontrado.')
            continue

        sleep(0.5)
        print('~' * 35)
        for i, (k, v) in enumerate(pessoa.items()):
            print(f'{i} - {k.ljust(12)} {v}')
        print('~' * 35)

        sleep(1)
        try:
            escolha_editar = int(input('Digite o número do dado que deseja mudar: '))
            chave = list(pessoa.keys())[escolha_editar]
        except (ValueError, IndexError):
            print('Opção inválida.')
            continue

        # Permite editar apenas um campo específico do cadastro
        if chave == 'id':
            while True:
                try:
                    novo_id = int(input('Novo ID numérico: '))
                    if id_existe(grupo, novo_id):
                        print('Esse ID já está em uso.')
                    else:
                        pessoa['id'] = novo_id
                        print('ID atualizado com sucesso!')
                        break
                except ValueError:
                    print('ID inválido.')
        else:
            if chave == 'nascimento':
                try:
                    nova_data = datetime.strptime(novo_valor := input(
                        'Nova data de nascimento (DD/MM/AAAA): '
                    ), '%d/%m/%Y').date()

                    hoje = date.today()
                    idade = hoje.year - nova_data.year
                    if (hoje.month, hoje.day) < (nova_data.month, nova_data.day):
                        idade -= 1

                    pessoa['nascimento'] = nova_data.strftime('%d/%m/%Y')
                    pessoa['idade'] = idade
                    print('Data de nascimento e idade atualizadas com sucesso!')

                except ValueError:
                    print('Data inválida. Edição cancelada.')
            else:
                novo_valor = input(f'Novo valor para {chave}: ').strip()
                pessoa[chave] = novo_valor
                print('Cadastro atualizado com sucesso!')

    elif escolha == '8':
        try:
            id_excluir = int(input('Digite o ID do usuário para excluir: '))
        except ValueError:
            print('ID inválido.')
            continue

        pessoa = buscar_pessoa_por_id(grupo, id_excluir)

        if pessoa is None:
            print('Usuário não encontrado.')
            continue
        
        sleep(0.5)
        print('~' * 35)
        for k, v in pessoa.items():
            print(f'{k.ljust(12)} {v}')
        print('~' * 35)

        while True:
            escolha_exclusao = str(input('Deseja mesmo excluir esse cadastro? [S/N] ')).strip().upper()[0]
            sleep(0.5)
            if escolha_exclusao in 'SN':
                break
            print('Opção inválida! Digite S ou N')
        if escolha_exclusao == 'S':
            grupo.remove(pessoa)
            print('Cadastro excluído com sucesso!')
        else:
            print('Exclusão cancelada!')

    elif escolha == '9':
        sleep(0.5)
        print('Saindo...')
        break

sleep(1)
print('<<< ATÉ BREVE >>>')