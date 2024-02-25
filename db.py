import json
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
load_dotenv()
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}
def conectar_db():
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None  

def inserir_anime_db(nome, ultimo_episodio, plataforma, id_externo):
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor() as cursor:
            cursor.execute('INSERT INTO anime (name_anime, ultimo_ep, plataforma, id_externo) VALUES (%s, %s, %s, %s)', (nome, ultimo_episodio, plataforma, id_externo))
    conexao.close()

def listar_animes_db():
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute('SELECT * FROM anime a JOIN plataforma p ON a.plataforma = p.id_plataforma WHERE a.ativo = true')
            animes = cursor.fetchall()
            return animes
    conexao.close()

def atualizar_ep_anime_db(id_anime, ultimo_episodio):
    if len(str(ultimo_episodio)) < 2:
        ultimo_episodio = '00' + str(ultimo_episodio)
    if len(str(ultimo_episodio)) < 3:
        ultimo_episodio = '0' + str(ultimo_episodio)
    else:
        ultimo_episodio = str(ultimo_episodio)
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute('UPDATE anime SET ultimo_ep = %s WHERE id_anime = %s', (ultimo_episodio, id_anime))
    conexao.close()
    print('ultimo episodio atualizado')

def listar_dowloads_db():
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute('SELECT * FROM dowloads JOIN anime ON dowloads.id_anime = anime.id_anime ORDER BY dowloads.id_anime, dowloads.numero_ep ASC')
            dowloads = cursor.fetchall()
            return dowloads
    conexao.close()

def buscar_anime_db(id_anime):
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute('SELECT * FROM anime a JOIN plataforma p ON a.plataforma = p.id_plataforma WHERE a.id_anime = %s ', (id_anime,))
            anime = cursor.fetchone()
            return anime
    conexao.close()

def listar_todos_dowloads():
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute('SELECT * FROM dowloads') 
            dowload = cursor.fetchall()
            return dowload
    conexao.close()
def escrever_dados(stor):
    with open('/home/vitor/ads/teste_py/stor.json', 'w') as file:
        json.dump(stor, file)

def ler_dados():
    with open('/home/vitor/ads/teste_py/stor.json', 'r') as file:
        dados = json.load(file)
        return dados