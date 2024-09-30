import os
import sqlite3
from time import process_time, process_time_ns
from traceback import print_tb

import pandas as pd
import csv
import shutil
from datetime import datetime
import textwrap

def criar_diretorios():
    os.makedirs('./meu_sistema_livraria/data', exist_ok=True)
    os.makedirs('./meu_sistema_livraria/exports', exist_ok=True)
    os.makedirs('./meu_sistema_livraria/backups', exist_ok=True)
    os.makedirs('./meu_sistema_livraria/imports', exist_ok=True)

def criar_conexao():
    conexao = sqlite3.connect('./meu_sistema_livraria/data/livraria.db')
    return conexao

def criar_tabela(conexao):
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo VARCHAR(100) NOT NULL,
            autor VARCHAR(100) NOT NULL,
            ano_publicado INTEGER NOT NULL,
            preco DECIMAL (10, 2) NOT NULL
        )
    ''')
    conexao.commit()
    return cursor

def cria_arquivo_csv(cursor):
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()

    with open('./meu_sistema_livraria/exports/livros_exportados.csv', 'w', newline='', encoding='UTF-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'titulo', 'autor', 'ano_publicado', 'preço'])

        for livro in livros:
            writer.writerow(livro)

def mostrar_csv():
    arquivo = pd.read_csv('./meu_sistema_livraria/exports/livros_exportados.csv')
    print('\n', arquivo.to_string(index=False))

def criar_backup():
    data = datetime.now().strftime('%d-%m-%Y')
    nome = f'backup_livraria_{data}.db'
    caminho = os.path.join('./meu_sistema_livraria/backups', nome)
    shutil.copy2('./meu_sistema_livraria/data/livraria.db', caminho)
    print(f'Backup criado: {caminho}')

def tira_backup():
    arquivos_backup = [f for f in os.listdir('./meu_sistema_livraria/backups') if f.startswith('backup_livraria_') and f.endswith('.db')]

    if len(arquivos_backup) > 5:
        arquivos_backup = [os.path.join('./meu_sistema_livraria/backups', f) for f in arquivos_backup]
        arquivos_backup.sort(key=os.path.getmtime)

        for arquivo_antigo in arquivos_backup[:-5]:
            os.remove(arquivo_antigo)
            print(f"Backup removido: {arquivo_antigo}")

def backup():
    criar_backup()
    tira_backup()

def relatorio():
    while True:
        selecao = int(input(textwrap.dedent(f'''
            {'-'*15} GERAR RELATÓRIO {'-'*15}
            
            [1] Gerar em HTML
            [2] Gerar em XML
            [3] Sair
            
            Digite o número desejado: ''')))

        if selecao == 1:
            try:
                arquivo = pd.read_csv('./meu_sistema_livraria/exports/livros_exportados.csv')
                arquivo.to_html('./meu_sistema_livraria/exports/livros_exportados.html')
                print('Arquivo HTML gerado com sucesso!')
            except FileNotFoundError:
                print('Gere um arquivo CSV primeiro!')

        elif selecao == 2:
            try:
                arquivo = pd.read_csv('./meu_sistema_livraria/exports/livros_exportados.csv')
                arquivo.to_xml('./meu_sistema_livraria/exports/livros_exportados.xml', parser='etree')
                print('Arquivo XML gerado com sucesso!')
            except FileNotFoundError:
                print('Gere um arquivo CSV primeiro!')

        elif selecao == 3:
            break

        else:
            print('\nA opção não é válida! Digite novamente o número.')

def fechar_conexao(conexao):
    conexao.close()
