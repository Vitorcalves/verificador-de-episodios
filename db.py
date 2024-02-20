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

def escrever_dados(stor):
    with open('/home/vitor/ads/teste_py/stor.json', 'w') as file:
        json.dump(stor, file)

def ler_dados():
    with open('/home/vitor/ads/teste_py/stor.json', 'r') as file:
        dados = json.load(file)
        return dados