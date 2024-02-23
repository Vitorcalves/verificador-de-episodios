from dowload import dowload_ep_db
import requests
import uuid
import subprocess
import os
from psycopg2.extras import RealDictCursor
import psycopg2
import threading
import re

from db import ler_dados, escrever_dados, conectar_db

def adicionar_anime_db():
    conexao = conectar_db()
    if conexao == None:
        print("falha na conexao com banco")
        return
    with conexao:
        with conexao.cursor() as cursor:
            print("adicionar anime")
            print("digite o nome do anime")
            nome = input()
            print("digite o id externo")
            id_externo = int(input())
            print("digite o id da plataforma")
            plataforma = int(input())
            print("possibilidade player? 1 - sim, 2 - nao")
            opcao = int(input())
            print("digite o numero do ultimo episodio ou deixe em branco e sera considerado 0")
            ultimo_episodio = input()
            if ultimo_episodio == "":
                ultimo_episodio = 0
            else:
                ultimo_episodio = int(ultimo_episodio)
            cursor.execute("INSERT INTO anime (name_anime, ultimo_ep, plataforma, id_externo) VALUES (%s, %s, %s, %s)", (nome, ultimo_episodio, plataforma, id_externo))
    conexao.close()

def remover_anime_db():
    conexao = conectar_db()
    if conexao == None:
        print("falha na conexao com banco")
        return
    with conexao:
        with conexao.cursor() as cursor:
            print("remover anime")
            cursor.execute("SELECT id_anime, name_anime FROM anime WHERE ativo = true")
            animes = cursor.fetchall()
            print("digite o id do anime")
            id = int(input())
            cursor.execute("UPDATE anime SET ativo = false WHERE id_anime = %s", (id,))

    conexao.close()

def listar_ep_anime_db():
    conexao = conectar_db()
    if conexao == None:
        print("falha na conexao com banco")
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            print("listar episodios anime")
            cursor.execute("SELECT id_anime, name_anime FROM anime WHERE ativo = true")
            animes = cursor.fetchall()
            for anime in animes:
                print(f'ID {anime["id_anime"]} Nome {anime["name_anime"]}')
            print("digite o id do anime")
            id = int(input())
            for anime in animes:
                if anime["id_anime"] == id:
                    cursor.execute("SELECT * FROM anime a JOIN plataforma p ON a.plataforma = p.id_plataforma WHERE a.id_anime = %s ", (anime["id_anime"],))
                    anime = cursor.fetchall()
                    url_api = anime[0]["link_api"].replace("{id_externo}", str(anime[0]["id_externo"]))
                    response = requests.get(url_api)
                    if response.status_code == 200:
                        data = response.json()
                        print("****************************")
                        print(anime[0]["name_anime"])
                        print("****************************")
                        for episode in data['data']:
                            print(f"Episódio {episode['n_episodio']}: {episode['titulo_episodio']}")
                            print(f"Data de Lançamento: {episode['data_registro']}")
                            print(anime[0]["link_plataforma"] + episode["generate_id"] + "/")
                            print("---")
                        print("deseja assistir ou baixar algum episodio? 0-cancelar 1 - baixar, 2 - assistir")
                        opcao = int(input())
                        if opcao == 1:
                            print("digite o numero do episodio")
                            numero_ep = int(input())
                            for episode in data['data']:
                                if int(episode['n_episodio']) == numero_ep:
                                    link_dowload = anime[0]["link_dowloads"].replace("{'slug_serie'}", anime[0]["slug_serie"]).replace("{'n_episodio'}", episode['n_episodio'])
                                    dowload_ep_db(link_dowload, anime[0]["id_anime"], episode['n_episodio'], episode['titulo_episodio'])
                        elif opcao == 2:
                            print("digite o numero do episodio")
                            numero_ep = int(input())
                            for episode in data['data']:
                                if int(episode['n_episodio']) == numero_ep:
                                    link_dowload = anime[0]["link_dowloads"].replace("{'slug_serie'}", anime[0]["slug_serie"]).replace("{'n_episodio'}", episode['n_episodio'])
                                    assistir_ep_anime_db(link_dowload, episode['n_episodio'], anime[0]["id_anime"])
                    else:
                        print("##############################")
                        print("Falha na requisição")
                        print("##############################")

                    break

    conexao.close()

def assistir_ep_anime_db(link_dowload, numero_ep, id_anime):
    heder = {'Referer': 'https://www.anroll.net/'}
    bJson = requests.get(link_dowload, headers=heder)
    if bJson.status_code == 200:
        data = bJson.text
        id = str(uuid.uuid4())
        caminho = '/tmp/' + id + '.m3u8'
        caminho_mp4 = '/tmp/' + id + '.mp4'
        with open(caminho, 'w') as file:
            file.write(data)
        subprocess.run(["vlc", caminho])
        atualizar_ep_anime_db(id_anime, numero_ep)
    else:
        print("falha na conexao")     

def atualizar_ep_anime_db(id_anime, ultimo_episodio):
    if len(str(ultimo_episodio)) < 2:
        ultimo_episodio = "00" + str(ultimo_episodio)
    if len(str(ultimo_episodio)) < 3:
        ultimo_episodio = "0" + str(ultimo_episodio)
    else:
        ultimo_episodio = str(ultimo_episodio)
    conexao = conectar_db()
    if conexao == None:
        print("falha na conexao com banco")
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("UPDATE anime SET ultimo_ep = %s WHERE id_anime = %s", (ultimo_episodio, id_anime))
    conexao.close()
    print("ultimo episodio atualizado")

def listar_dowloads_db():
    conexao = conectar_db()
    if conexao == None:
        print("falha na conexao com banco")
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM dowloads JOIN anime ON dowloads.id_anime = anime.id_anime")
            dowloads = cursor.fetchall()
            for dowload in dowloads:
                print(dowload["id_dowloads"])
                print(dowload["id_anime"])
                print(dowload["name_anime"])
                print(dowload["numero_ep"])
                print(dowload["titulo_ep"])
                print("********************")
            print("digite o id do dowload")
            id = input()
            print("deseja assistir ou apagar? 1 - assistir, 2 - apagar 0 - cancelar")
            opcao = int(input())
            if opcao == 1:
                for dowload in dowloads:
                    if dowload["id_dowloads"] == id:
                        caminho = '/home/vitor/dowloads_animes/' + id + '.mp4'
                        subprocess.run(["vlc", caminho])
                        atualizar_ep_anime_db(dowload["id_anime"], dowload["numero_ep"])
                        cursor.execute("UPDATE dowloads SET assistido = true WHERE id_dowloads = %s", (id,))
            elif opcao == 2:
                apagar_dowloads(id)
            else:
                print("cancelado")
    conexao.close()

def verificar_ep_db():
    conexao = conectar_db()
    if conexao == None:
        print("falha na conexao com banco")
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM anime a JOIN plataforma p ON a.plataforma = p.id_plataforma WHERE a.ativo = true")
            animes = cursor.fetchall()
            for anime in animes:
                response = requests.get(anime["link_api"].replace("{id_externo}", str(anime["id_externo"])))
                novo_ep = False
                if response.status_code == 200:
                    data = response.json()
                    print("****************************")
                    print(anime["name_anime"])
                    print("****************************")
                    for episode in data['data']:
                        if int(episode['n_episodio']) > int(anime["ultimo_ep"]):
                            print(f"Episódio {episode['n_episodio']}: {episode['titulo_episodio']}")
                            print(f"Data de Lançamento: {episode['data_registro']}")
                            print(anime["link_plataforma"] + episode["generate_id"] + "/")
                            novo_ep = True
                            print("---")
                            print("deseja atualizar o ultimo episodio? 0 - parar, 1 - sim,  2 - nao, 3 - assistir, 4 - baixar")
                            opcao = int(input())
                            if opcao == 1:
                                atualizar_ep_anime_db(anime["id_anime"], episode['n_episodio'])
                            elif opcao == 0:
                                break
                            elif opcao == 3:
                                assistir_ep_anime_db(anime["link_dowloads"].replace("{'slug_serie'}", anime["slug_serie"]).replace("{'n_episodio'}", episode['n_episodio']),
                                episode['n_episodio'], anime["id_anime"])
                            elif opcao == 4:
                                dowload_ep_db(anime["link_dowloads"].replace("{'slug_serie'}", anime["slug_serie"]).replace("{'n_episodio'}", episode['n_episodio']), anime["id_anime"], episode['n_episodio'], episode['titulo_episodio'])
                            else:
                                print("ultimo episodio nao atualizado")
                    if not novo_ep:
                        print("sem novos episodios")
                else:
                    print("##############################")
                    print("Falha na requisição")
                    print("##############################")
    conexao.close()

def listar_novos_ep_db():
    conexao = conectar_db()
    if conexao == None:
        print("falha na conexao com banco")
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM anime a JOIN plataforma p ON a.plataforma = p.id_plataforma WHERE a.ativo = true")
            animes = cursor.fetchall()
            for anime in animes:
                try:
                    response = requests.get(anime["link_api"].replace("{id_externo}", str(anime["id_externo"])), timeout=10)
                    novo_ep = False
                    if response.status_code == 200:
                        data = response.json()
                        print("****************************")
                        print(anime["name_anime"])
                        print("****************************")
                        for episode in data['data']:
                            if int(episode['n_episodio']) > int(anime["ultimo_ep"]):
                                print(f"Episódio {episode['n_episodio']}: {episode['titulo_episodio']}")
                                print(f"Data de Lançamento: {episode['data_registro']}")
                                print(anime["link_plataforma"] + episode["generate_id"] + "/")
                                novo_ep = True
                                print("---")
                        if not novo_ep:
                            print("sem novos episodios")
                    else:
                        print("##############################")
                        print("Falha na requisição")
                        print("##############################")
                except requests.exceptions.Timeout:
                     print(f"Timeout na requisição para {anime['name_anime']}")
    conexao.close()

def editar_anime_db():
    conexao = conectar_db()
    if conexao == None:
        print("falha na conexao com banco")
        return
    with conexao:
        with conexao.cursor() as cursor:
            print("editar anime")
            cursor.execute("SELECT id_anime, name_anime, ultimo_ep  FROM anime WHERE ativo = true")
            animes = cursor.fetchall()
            for anime in animes:
                print(f'ID = {anime[0]} Nome {anime[1]} ultimo episodio {anime[2]}')
            print("digite o id do anime")
            id = int(input())
            print("digite o novo numero do ultimo episodio")
            ultimo_episodio = int(input())
            atualizar_ep_anime_db(id, ultimo_episodio)

    conexao.close()
