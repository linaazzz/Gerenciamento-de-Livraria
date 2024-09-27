import pandas as pd
import functions
import textwrap

def main():
    conexao = functions.criar_conexao()
    cursor = conexao.cursor()
    functions.criar_tabela(conexao)

    while True:
        try:
            selecao = int(input(textwrap.dedent(f"""
                {'-'*15} MENU {'-'*15}
                
                [1] Adicionar novo livro
                [2] Exibir todos os livros
                [3] Atualizar preço de um livro
                [4] Remover um livro
                [5] Buscar livros por autor
                [6] Exportar dados para CSV
                [7] Importar dados de CSV
                [8] Fazer backup do banco de dados
                [9] Sair
                    
                Digite o número desejado: """)))

            if selecao == 1:
                print(f'\n{'-'*15} ADICIONAR NOVO LIVRO {'-'*15}')
                novo_livro = []

                try:
                    novo_livro.append(input('\nDigite o título do seu livro: '))
                    novo_livro.append(input('Digite o autor do seu livro: '))
                    novo_livro.append(int(input('Digite o ano de publicação do seu livro: ')))
                    novo_livro.append(float(input('Digite o preço do seu livro: ')))

                    cursor.execute('''
                        INSERT INTO livros (titulo, autor, ano_publicado, preco) VALUES (?,?,?,?)
                    ''', (novo_livro[0], novo_livro[1], novo_livro[2], novo_livro[3]))

                    print('\nNovo livro adicionado com sucesso!')
                    functions.backup()
                    conexao.commit()
                except ValueError:
                    print("\nPor favor, insira valores válidos!")
                except Exception as e:
                    print(f"\nErro ao adicionar livro: {e}")

            elif selecao == 2:
                cursor.execute('SELECT * FROM livros')
                elementos = cursor.fetchall()

                if elementos:
                    tabela = pd.DataFrame(elementos, columns=['ID', 'Título', 'Autor', 'Ano Publicado', 'Preço'])
                    print(tabela.to_string(index=False))
                else:
                    print('A lista está vazia.')

            elif selecao == 3:
                print(f'\n{'-' * 15} ALTERAR PREÇO {'-' * 15}')
                try:
                    cursor.execute('SELECT * FROM livros')
                    resultado = cursor.fetchall()

                    while True:
                        titulo = input('\nDigite o título do livro que terá o preço alterado ou digite sair para cancelar: ')

                        if titulo == 'sair':
                            break

                        titulo_encontrado = False

                        for nome in resultado:
                            if titulo == nome[1]:
                                print('Título encontrado!')
                                titulo_encontrado = True
                                break

                        if titulo_encontrado:
                            preco = float(input(f'Digite o novo valor do livro "{titulo}": '))

                            cursor.execute('''
                                UPDATE livros SET preco = ? WHERE titulo = ?
                            ''', (preco, titulo))

                            print(f'Preço do livro "{titulo}" atualizado para R${preco:.2f}')
                            functions.backup()
                            conexao.commit()
                            break
                        else:
                            print('O título digitado não foi encontrado. Digite novamente.')
                except ValueError: print('Digite um valor válido!')

            elif selecao == 4:
                print(f'\n{'-' * 15} DELETAR LIVRO {'-' * 15}')
                try:
                    cursor.execute('SELECT * FROM livros')
                    resultado = cursor.fetchall()

                    while True:
                        titulo = input('\nDigite o título do livro que será deletado ou digite "sair" para cancelar: ')

                        if titulo == 'sair':
                            break

                        titulo_encontrado = False

                        for nome in resultado:
                            if titulo == nome[1]:
                                print('Título encontrado!')
                                titulo_encontrado = True
                                break

                        if titulo_encontrado:
                            cursor.execute('''
                                            DELETE FROM livros WHERE titulo = ?
                            ''', (titulo, ))

                            print(f'O livro "{titulo}" foi deletado com sucesso!')
                            functions.backup()
                            conexao.commit()
                            break
                        else:
                            print('O título digitado não foi encontrado. Digite novamente.')
                except ValueError:
                    print('Digite um valor válido!')

            elif selecao == 5:
                print(f'\n{'-' * 15} BUSCA DE LIVROS {'-' * 15}')
                cursor.execute('SELECT * FROM livros')
                resultado = cursor.fetchall()

                while True:
                    autor = input('\nDigite o nome do autor para a busca de livros ou digite "sair" para cancelar: ')

                    if autor == 'sair':
                        break

                    autor_encontrado = False

                    for nome in resultado:
                        if autor == nome[2]:
                            print(f'Nome do livro: {nome[1]}')
                            autor_encontrado = True

                    if autor_encontrado:
                        break
                    else:
                        print('Nome do autor não encontrado. Digite novamente.')

            elif selecao == 6:
                print(f'\n{'-' * 15} EXPORTAR DADOS {'-' * 15}')
                functions.cria_arquivo_csv(cursor)
                print('Operação efetuada com sucesso!')

            elif selecao == 7:
                while True:
                    print(f'\n{'-' * 15} IMPORTAR DADOS {'-' * 15}')
                    nome = input('\nDigite o nome do arquivo (sem ".csv") a ser importado da pasta "imports": ')
                    caminho = f'./meu_sistema_livraria/imports/{nome}.csv'

                    try:
                        arquivo = pd.read_csv(caminho)

                        if 'id' in arquivo.columns:
                            arquivo = arquivo.drop(columns=['id'])

                        arquivo.to_sql('livros', conexao, if_exists='append', index=False)
                        print('Dados inseridos no banco de dados com sucesso!')
                        functions.backup()
                        conexao.commit()
                    except ValueError:
                        print('Arquivo não encontrado!')

            elif selecao == 8:
                functions.backup()

            elif selecao == 9: break

            else:
                print('\nA opção não é válida! Digite novamente o número.')

        except ValueError:
            print("\nPor favor, insira um número inteiro!")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    functions.fechar_conexao(conexao)

if __name__ == '__main__':
    functions.criar_diretorios()
    main()
