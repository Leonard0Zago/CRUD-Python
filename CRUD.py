# -*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error, OperationalError
import os
from time import sleep
import locale
locale.setlocale(locale.LC_MONETARY, 'pt_BR')
locale.setlocale(locale.LC_NUMERIC, 'pt_BR')


def exibir_cabecalho(mensagem):
    mensagem = f'Rotina de {mensagem} de dados'

    print('\n' + '-' * len(mensagem))
    print(mensagem)
    print('\n' + '-' * len(mensagem))

    id = input('ID (0 para voltar): ')

    return id

def conectarBanco():
    conexao = None
    banco = 'unoesc2.db'

    print(f'SQLite versão: {sqlite3.version}\n')

    path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(path, banco)
    print(f'Banco de dados: [{full_path}]\n')

    if not os.path.isfile(full_path):
        continuar = input(
            f'Banco de dados não encontrado, deseja criá-lo? \nSe sim, então o banco de dados será criado no diretório onde o programa está sendo executado [{os.getcwd()}]! [S/N]: ')

        if continuar.upper() != 'S':
            raise sqlite3.DatabaseError('Banco de dados não selecionado!')

    conexao = sqlite3.connect(full_path)
    print('BD aberto com sucesso!')

    return conexao

def criar_tabela(conexao):
    cursor = conexao.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS funcionarios (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome TEXT,
                       data TEXT,
                       salario SALARY
                   )
                   """)
    conexao.commit()

    if cursor:
        cursor.close()

def incluir(conexao):
    id = exibir_cabecalho('inclusão')
    if int(id) == 0:
        return

    if verificar_registro_existe(conexao, id):
        print('\nID já existe!')
        sleep(2)
    else:
        nom = input('\nNome: ')
        dat = input('\nData nascimento: ')
        sal = input('\nSalário: ')
        confirma = input('\nConfirma a inclusão [S/N]? ').upper()

        if confirma == 'S':
            comando = f'INSERT INTO funcionarios VALUES({id}, "{nom}", "{dat}", "{sal}")'
            print(comando)
            cursor = conexao.cursor()
            cursor.execute(comando)
            conexao.commit()
            cursor.close()

def alterar(conexao):
    if tabela_vazia(conexao):
        print('\n*** TABELA VAZIA ***')
        pausa()
        return

    id = exibir_cabecalho('alteração')
    if int(id) == 0:
        return

    resultado = verificar_registro_existe(conexao, id)
    if not resultado:
        print('\nID não existe!')
        sleep(2)
    else:
        mostrar_registro(resultado)

        nom = input('\nNome: ')
        dat = input('\nData nascimento: ')
        sal = input('\nSalário: ')
        confirma = input('\nConfirma a alteração [S/N]? ').upper()

        if confirma == 'S':
            cursor = conexao.cursor()
            cursor.execute('UPDATE funcionarios SET nome=?WHERE id=?', (nom, id))
            cursor.execute('UPDATE funcionarios SET data=?WHERE id=?', (dat, id))
            cursor.execute('UPDATE funcionarios SET salario=?WHERE id=?', (sal, id))
            conexao.commit()
            cursor.close()

def listar(conexao):
    if tabela_vazia(conexao):
        print('\n*** TABELA VAZIA ***')
        pausa()
        return

    print('\n----------------------')
    print('Listagem dos Registros')
    print('----------------------\n')

    cursor = conexao.execute('SELECT * from funcionarios')
    registros = cursor.fetchall()

    for registro in registros:
        print('ID..:', registro[0])
        print('Nome:', registro[1])
        print('Data:', registro[2])
        print('Salário:', registro[3])
        print('-----')

    pausa()

    cursor.close()
    
def pesquisa(conexao):
    
    opcao = 0
    
    while opcao != 5:

        print('--------------')
        print('O que deseja pesquisar?')
        print('--------------')
        print('1. Por ID')
        print('2. Por nome')
        print('3. Pela data de nascimento')
        print('4. Pelo salário')
        print('5. Sair')

        try:
            opcao = int(input('\nOpção [1-5]: '))
        except ValueError:
            opcao <= 0
        except ValueError:
            opcao > 5

        if opcao == 1:
            
            pesq = input('\nPesquisar: ')
            
            cursor = conexao.execute('SELECT * FROM funcionarios WHERE nome LIKE ?', (f'%{pesq}%'))
            registros = cursor.fetchall()
            cursor.close()
            for registro in registros:
                print('-----')
                print('ID..:', registro[0])
                print('Nome:', registro[1])
                print('Data:', registro[2])
                print('Salário:', registro[3])
                print('-----')
            
        elif opcao == 2:
            
            pesq = input('\nPesquisar: ')
            
            cursor = conexao.execute('SELECT * FROM funcionarios WHERE nome LIKE ?', (f'%{pesq}%'))

            registros = cursor.fetchall()
            cursor.close()
            for registro in registros:
                print('-----')
                print('ID..:', registro[0])
                print('Nome:', registro[1])
                print('Data:', registro[2])
                print('Salário:', registro[3])
                print('-----')
            
        elif opcao == 3:
            
            pesq = input('\nPesquisar: ')
            
            cursor = conexao.execute('SELECT * FROM funcionarios WHERE data LIKE ?', (f'%{pesq}%'))
            registros = cursor.fetchall()
            for registro in registros:
                print('-----')
                print('ID..:', registro[0])
                print('Nome:', registro[1])
                print('Data:', registro[2])
                print('Salário:', registro[3])
                print('-----')
            
        elif opcao == 4:
            
            pesq = input('\nPesquisar: ')
            
            cursor = conexao.execute('SELECT * FROM funcionarios WHERE salario LIKE ?', (f'%{pesq}%'))
            registros = cursor.fetchall()
            cursor.close()
            for registro in registros:
                print('-----')
                print('ID..:', registro[0])
                print('Nome:', registro[1])
                print('Data:', registro[2])
                print('Salário:', registro[3])
                print('-----')
            
        elif opcao == 5:
            break

        print()

    return opcao

def excluir(conexao):
    if tabela_vazia(conexao):
        print('\n*** TABELA VAZIA ***')
        pausa()
        return

    id = exibir_cabecalho('alteração')
    if int(id) == 0:
        return

    resultado = verificar_registro_existe(conexao, id)
    if not resultado:
        print('\nID não existe!')
        sleep(2)
    else:
        mostrar_registro(resultado)

        confirma = input('\nConfirma a exclusão [S/N]? ').upper()

        if confirma == 'S':
            cursor = conexao.cursor()
            cursor.execute('DELETE FROM funcionarios WHERE id=?', (id,))
            conexao.commit()
            cursor.close()

def mostrar_registro(registro):
    print('\n====================')
    print('Registro')
    print('--------')
    print('ID..:', registro[0])
    print('Nome:', registro[1])
    print('Data:', registro[2])
    print('Salário:', registro[3])
    print('====================')

def tabela_vazia(conexao):
    cursor = conexao.cursor()
    cursor.execute('SELECT count(*) FROM funcionarios')
    resultado = cursor.fetchall()
    cursor.close()

    return resultado[0][0] == 0

def verificar_registro_existe(conexao, id):
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM funcionarios WHERE id=?', (id))
    resultado = cursor.fetchone()
    cursor.close()

    return resultado

def pausa():
    input('\nPressione <ENTER> para continuar')

def menu(conexao):
    opcao = 1
    while opcao != 6:

        print('--------------')
        print('MENU DE OPÇÕES')
        print('--------------')
        print('1. Incluir dados')
        print('2. Alterar dados')
        print('3. Excluir dados')
        print('4. Listar dados')
        print('5. Pesquisar dados')
        print('6. Sair')

        try:
            opcao = int(input('\nOpção [1-6]: '))
        except ValueError:
            opcao = 0

        if opcao == 1:
            incluir(conexao)
        elif opcao == 2:
            alterar(conexao)
        elif opcao == 3:
            excluir(conexao)
        elif opcao == 4:
            listar(conexao)
        elif opcao == 5:
            pesquisa(conexao)
        elif opcao != 6:
            print('Opção inválida, tente novamente')
            sleep(2)

        print()

    return opcao

if __name__ == '__main__':
    conn = None

    while True:
        try:
            conn = conectarBanco()
            criar_tabela(conn)

            # incluirUmRegistro(conn)
            # incluirVariosRegistros(conn)

            if menu(conn) == 6:
                break
        except OperationalError as e:
            print('Erro operacional:', e)
        except sqlite3.DatabaseError as e:
            print('Erro database:', e)
            # Não mostra o traceback
            raise SystemExit()
        except Error as e:
            print('Erro SQLite3:', e)
            # Não mostra o traceback
            raise SystemExit()
        except Exception as e:
            print('Erro durante a execução do sistema!')
            print(e)
        finally:
            if conn:
                print('Liberando a conexão...')
                conn.commit()
                conn.close()

    print('Encerrando...')
