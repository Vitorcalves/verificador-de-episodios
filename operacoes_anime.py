from dowload import dowload_ep_db
import requests
import uuid
import subprocess
import os

from db import conectar_db, inserir_anime_db, listar_animes_db, atualizar_ep_anime_db, listar_dowloads_db

def adicionar_anime():
    print('adicionar anime')
    print('digite o nome do anime')
    nome = input()
    print('digite o id externo')
    id_externo = int(input())
    print('digite o id da plataforma')
    plataforma = int(input())
    print('slug da serie')
    slug_serie = input()
    print('digite o numero do ultimo episodio ou deixe em branco e sera considerado 0')
    ultimo_episodio = input()
    if ultimo_episodio == '':
        ultimo_episodio = '000'
    inserir_anime_db(nome, plataforma, id_externo, slug_serie, ultimo_episodio)

def remover_anime_db():
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor() as cursor:
            print('remover anime')
            print('digite o id do anime')
            id = int(input())
            cursor.execute('UPDATE anime SET ativo = false WHERE id_anime = %s', (id,))

    conexao.close()

def listar_ep_anime_db():
    animes = listar_animes_db()
    for anime in animes:
        print(f'ID {anime["id_anime"]} Nome {anime["name_anime"]}')
    print('digite o id do anime')
    id = int(input())
    for anime in animes:
        if anime['id_anime'] == id:
            url_api = anime['link_api'].replace('{id_externo}', str(anime['id_externo']))
            response = requests.get(url_api)
            if response.status_code == 200:
                data = response.json()
                print('****************************')
                print(anime['name_anime'])
                print('****************************')
                for episode in data['data']:
                    print(f'Episódio {episode["n_episodio"]}: {episode["titulo_episodio"]}')
                    print(f'Data de Lançamento: {episode["data_registro"]}')
                    print(anime['link_plataforma'] + episode['generate_id'] + '/')
                    print('---')
                print('deseja assistir ou baixar algum episodio? 0-cancelar 1 - baixar, 2 - assistir')
                opcao = int(input())
                if opcao == 1:
                    print('digite o numero do episodio')
                    numero_ep = int(input())
                    for episode in data['data']:
                        if int(episode['n_episodio']) == numero_ep:
                            link_dowload = anime['link_dowloads'].replace("{'slug_serie'}", anime['slug_serie']).replace("{'n_episodio'}", episode['n_episodio'])
                            dowload_ep_db(link_dowload, anime['id_anime'], episode['n_episodio'], episode['titulo_episodio'])
                elif opcao == 2:
                    print('digite o numero do episodio')
                    numero_ep = int(input())
                    for episode in data['data']:
                        if int(episode['n_episodio']) == numero_ep:
                            link_dowload = anime['link_dowloads'].replace("{'slug_serie'}", anime['slug_serie']).replace("{'n_episodio'}", episode['n_episodio'])
                            assistir_ep_anime_db(link_dowload, episode['n_episodio'], anime['id_anime'])
            else:
                print('##############################')
                print('Falha na requisição')
                print('##############################')

            break

def assistir_ep_anime_db(link_dowload, numero_ep, id_anime):
    heder = {'Referer': 'https://www.anroll.net/'}
    bJson = requests.get(link_dowload, headers=heder)
    if bJson.status_code == 200:
        data = bJson.text
        id = str(uuid.uuid4())
        caminho = '/tmp/' + id + '.m3u8'
        with open(caminho, 'w') as file:
            file.write(data)
        subprocess.run(['vlc', caminho])
        atualizar_ep_anime_db(id_anime, numero_ep)
    else:
        print('falha na conexao')     

def listar_dowloads():
    while True:
        dowloads = listar_dowloads_db()
        cont = 0
        for dowload in dowloads:
            print(f'ID -  {cont}')
            print(f'Nome - {dowload["name_anime"]}')
            print(f'Numero EP - {dowload["numero_ep"]}')
            print(f'Titulo EP - {dowload["titulo_ep"]}')
            print(f'ID EP - {dowload["id_dowloads"]}')
            print('********************')
            cont += 1
        print('digite o id do dowload')
        try:
            id = int(input())
        except:
            print('id invalido')
            break
        if id > 0 or id <= len(dowloads):
            try:
                apisodio = dowloads[id]
            except:
                print('id invalido segundo try')
                continue
            print('deseja assistir ou apagar? 1 - assistir, 2 - apagar 0 - cancelar')
            opcao = int(input())
            if opcao == 1:
                caminho = '/home/vitor/dowloads_animes/' + apisodio['id_dowloads'] + '.mp4'
                subprocess.run(['vlc', caminho])
                atualizar_ep_anime_db(apisodio['id_anime'], apisodio['numero_ep'])
                print('deseja apagar o dowload? 1 - sim, 2 - nao')
                opcao = int(input())
                if opcao == 1:
                    apagar_dowloads(apisodio['id_dowloads'])
                else:
                    print('cancelado')
            elif opcao == 2:
                apagar_dowloads(apisodio['id_dowloads'])
            else:
                print('cancelado')
                break

def verificar_ep_db():
    animes = listar_animes_db()
    for anime in animes:
        response = requests.get(anime['link_api'].replace('{id_externo}', str(anime['id_externo'])))
        novo_ep = False
        if response.status_code == 200:
            data = response.json()
            print('****************************')
            print(anime['name_anime'])
            print('****************************')
            for episode in data['data']:
                if int(episode['n_episodio']) > int(anime['ultimo_ep']):
                    print(f'Episódio {episode["n_episodio"]}: {episode["titulo_episodio"]}')
                    print(f'Data de Lançamento: {episode["data_registro"]}')
                    print(anime['link_plataforma'] + episode['generate_id'] + '/')
                    novo_ep = True
                    print('---')
                    print('deseja atualizar o ultimo episodio? 0 - parar, 1 - sim,  2 - nao, 3 - assistir, 4 - baixar')
                    opcao = int(input())
                    if opcao == 1:
                        atualizar_ep_anime_db(anime['id_anime'], episode['n_episodio'])
                    elif opcao == 0:
                        break
                    elif opcao == 3:
                        assistir_ep_anime_db(anime['link_dowloads'].replace("{'slug_serie'}", anime['slug_serie']).replace("{'n_episodio'}", episode['n_episodio']),
                        episode['n_episodio'], anime['id_anime'])
                    elif opcao == 4:
                        dowload_ep_db(anime['link_dowloads'].replace("{'slug_serie'}", anime['slug_serie']).replace("{'n_episodio'}", episode['n_episodio']), anime['id_anime'], episode['n_episodio'], episode['titulo_episodio'])
                    else:
                        print('ultimo episodio nao atualizado')
            if not novo_ep:
                print('sem novos episodios')
        else:
            print('##############################')
            print('Falha na requisição')
            print('##############################')

def listar_novos_ep_db():
    animes = listar_animes_db()
    for anime in animes:
        try:
            response = requests.get(anime['link_api'].replace('{id_externo}', str(anime['id_externo'])), timeout=10)
            novo_ep = False
            if response.status_code == 200:
                data = response.json()
                print('****************************')
                print(anime['name_anime'])
                print('****************************')
                for episode in data['data']:
                    if int(episode['n_episodio']) > int(anime['ultimo_ep']):
                        print(f'Episódio {episode["n_episodio"]}: {episode["titulo_episodio"]}')
                        print(f'Data de Lançamento: {episode["data_registro"]}')
                        print(anime['link_plataforma'] + episode['generate_id'] + '/')
                        novo_ep = True
                        print('---')
                if not novo_ep:
                    print('sem novos episodios')
            else:
                print('##############################')
                print('Falha na requisição')
                print('##############################')
        except requests.exceptions.Timeout:
                print(f'Timeout na requisição para {anime["name_anime"]}')

def editar_anime_db():
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor() as cursor:
            print('editar anime')
            cursor.execute('SELECT id_anime, name_anime, ultimo_ep  FROM anime WHERE ativo = true')
            animes = cursor.fetchall()
            for anime in animes:
                print(f'ID = {anime[0]} Nome {anime[1]} ultimo episodio {anime[2]}')
            print('digite o id do anime')
            id = int(input())
            print('digite o novo numero do ultimo episodio')
            ultimo_episodio = int(input())
            atualizar_ep_anime_db(id, ultimo_episodio)

    conexao.close()

def apagar_dowloads(id_dowloads):
    conexao = conectar_db()
    if conexao is None:
        print('Falha no banco')
        return
    with conexao:
        with conexao.cursor() as cursor:
            try:
                os.remove(f'/home/vitor/dowloads_animes/{id_dowloads}.mp4')
            except Exception as e:
                print(f'Ocorreu um erro ao apagar o arquivo: {e}')
            try:
                cursor.execute('DELETE FROM dowloads WHERE id_dowloads = %s', (id_dowloads,))
            except Exception as e:
                print(f'Ocorreu um erro ao apagar registro no db: {e}')
    conexao.close()
