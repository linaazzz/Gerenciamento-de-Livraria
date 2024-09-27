import os
import sqlite3
import pandas as pd
import csv
import shutil
from datetime import datetime

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

def fechar_conexao(conexao):
    conexao.close()
