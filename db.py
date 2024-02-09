import json
from dotenv import load_dotenv
import os
import psycopg2
load_dotenv()
DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}
def conectar_db():
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

def ler_dowloads():
       with open('/home/vitor/ads/teste_py/dowloads.json', 'r') as file:
        dados = json.load(file)
        return dados 

def escrever_dowloads(stor):
    with open('/home/vitor/ads/teste_py/dowloads.json', 'w') as file:
        json.dump(stor, file)

def printar_dados():
    stor = ler_dados()
    for anime in stor:
        print(anime["id"], anime["nome"],anime["ultimo_episodio"])
    
def printar_banco():
    stor = ler_dados()
    for anime in stor:
        print(anime["id"], anime["nome"],anime["ultimo_episodio"], anime["api"], anime["link"])  

def escrever_dados(stor):
    with open('/home/vitor/ads/teste_py/stor.json', 'w') as file:
        json.dump(stor, file)

def escrever_delete( dado ):
    deletados = ler_delete()
    deletados.append(dado)
    with open('/home/vitor/ads/teste_py/delete.json', 'w') as file:
        json.dump(deletados, file)

def ler_delete():
    with open('/home/vitor/ads/teste_py/delete.json', 'r') as file:
        dados = json.load(file)
        return dados

def ler_dados():
    with open('/home/vitor/ads/teste_py/stor.json', 'r') as file:
        dados = json.load(file)
        return dados