import requests
import uuid
import subprocess
import os

from db import ler_dados, escrever_dados, escrever_delete, ler_dowloads, escrever_dowloads, ler_delete, printar_dados

def adicionar_anime():
    print("adicionar anime")
    store = ler_dados()
    print("digite o nome do anime")
    nome = input()
    print("digite link da API")
    api = input()
    print("digite o link do anime")
    link = input()
    print("possibilidade player? 1 - sim, 2 - nao")
    opcao = int(input())
    if opcao == 1:
        player = True
    else:
        player = False
    print("digite o numero do ultimo episodio ou deixe em branco e sera considerado 0")
    ultimo_episodio = input()
    if ultimo_episodio == "":
        ultimo_episodio = 0
    else:
        ultimo_episodio = int(ultimo_episodio)
    id = max([anime["id"] for anime in store], default=-1) + 1
    store.append({"id":id, "nome": nome, "api": api, "link": link, "ultimo_episodio": ultimo_episodio, "player": player})
    escrever_dados(store)

def remover_anime():
    print("remover anime")
    store = ler_dados()

    for anime in store:
        print(anime["id"], anime["nome"])

    print("digite 1 para digitar o id do anime ou 2 para digitar o nome")
    opcao = int(input())

    if opcao == 1:
        print("digite o id do anime")
        id = int(input())
        for anime in store:
            if anime["id"] == id:
                print(anime, "certeza que deseja remover? 1 - sim, 2 - nao")
                opcao = int(input())
                if opcao == 1:
                    escrever_delete(anime)
                    store.remove(anime)
                    escrever_dados(store)
                else:
                    print("anime nao removido")

    elif opcao == 2:
        print("digite o nome do anime")
        nome = input()
        for anime in store:
            if anime["nome"] == nome:
                print(anime, "certeza que deseja remover? 1 - sim, 2 - nao")
                opcao = int(input())
                if opcao == 1:
                    escrever_delete(anime)
                    store.remove(anime)
                    escrever_dados(store)
                else:
                    print("anime nao removido")
    
    else:
        print("opcao invalida")

def verificar_ep():
    store = ler_dados()
    continuar_verificacao = True
    for anime in store:
        if not continuar_verificacao:
            break
        response = requests.get(anime["api"])
        novo_ep = False
        if response.status_code == 200:
            data = response.json()
            print("**********************")
            print(anime["nome"])
            print("**********************")
            for episode in data['data']:
                if int(episode['n_episodio']) > anime["ultimo_episodio"]:
                    print(f"Episódio {episode['n_episodio']}: {episode['titulo_episodio']}")
                    print(f"Data de Lançamento: {episode['data_registro']}")
                    print(anime["link"] + episode["generate_id"] + "/")
                    novo_ep = True
                    print("---")
                    if not anime["player"]:
                        print("deseja atualizar o ultimo episodio? 0 - parar, 1 - sim,  2 - nao")
                        opcao = int(input())
                        if opcao == 1:
                            anime["ultimo_episodio"] = int(episode['n_episodio'])
                            escrever_dados(store)
                        elif opcao == 0:
                            continuar_verificacao = False
                            break
                        else:
                            print("ultimo episodio nao atualizado")
                    else:
                        print("deseja atualizar o ultimo episodio? 0 - parar, 1 - sim,  2 - nao, 3 - assistir")
                        opcao = int(input())
                        if opcao == 1:
                            anime["ultimo_episodio"] = int(episode['n_episodio'])
                            escrever_dados(store)
                        elif opcao == 0:
                            continuar_verificacao = False
                            break
                        elif opcao == 3:
                            heder = {'Referer': 'https://www.anroll.net/'}
                            bJson = requests.get(f"https://cdn-zenitsu-gamabunta.b-cdn.net/cf/hls/animes/{episode['anime']['slug_serie']}/{episode['n_episodio']}.mp4/media-1/stream.m3u8", headers=heder)
                            if bJson.status_code == 200:
                                data = bJson.text
                                caminho = '/tmp/' + str(uuid.uuid4()) + '.m3u8'
                                with open(caminho, 'w') as file:
                                    file.write(data)  
                                anime["ultimo_episodio"] = int(episode['n_episodio'])
                                escrever_dados(store)                    
                                subprocess.run(["vlc", caminho])
                            
                        else:
                            print("ultimo episodio nao atualizado")
            if not novo_ep:
                print("sem novos episodios")
        else:
            print("##############################")
            print("Falha na requisição")
            print("##############################")

def lista_ep():
    store = ler_dados()
    for anime in store:
        response = requests.get(anime["api"])
        novo_ep = False
        if response.status_code == 200:
            data = response.json()
            print("****************************")
            print(anime["nome"])
            print("****************************")
            for episode in data['data']:
                if int(episode['n_episodio']) > anime["ultimo_episodio"]:
                    print(f"Episódio {episode['n_episodio']}: {episode['titulo_episodio']}")
                    print(f"Data de Lançamento: {episode['data_registro']}")
                    print(anime["link"] + episode["generate_id"] + "/")
                    novo_ep = True
                    print("---")
                    
            if not novo_ep:
                print("sem novos episodios")
        else:
            print("##############################")
            print("Falha na requisição")
            print("##############################")

def editar_anime():
    store = ler_dados()
    printar_dados()
    print("digite o nome do anime")
    nome = input()
    for anime in store:
        if anime["nome"] == nome:
            print("digite o novo numero do ultimo episodio")
            ultimo_episodio = int(input())
            anime["ultimo_episodio"] = ultimo_episodio
            escrever_dados(store)
            break

def lista_ep_anime():
    store = ler_dados()
    printar_dados()
    print("digite o id do anime")
    id = int(input())
    for anime in store:
        if anime["id"] == id:
            response = requests.get(anime["api"])
            if response.status_code == 200:
                data = response.json()
                print("****************************")
                print(anime["nome"])
                print("****************************")
                for episode in data['data']:
                    print(f"Episódio {episode['n_episodio']}: {episode['titulo_episodio']}")
                    print(f"Data de Lançamento: {episode['data_registro']}")
                    print(anime["link"] + episode["generate_id"] + "/")
                    print("---")

def dowload_ep():
    store = ler_dados()
    for anime in store:
        response = requests.get(anime["api"])
        novo_ep = False
        if response.status_code == 200:
            data = response.json()
            print("****************************")
            print(anime["nome"])
            print("****************************")
            for episode in data['data']:
                if int(episode['n_episodio']) > anime["ultimo_episodio"]:
                    print(f"Episódio {episode['n_episodio']}: {episode['titulo_episodio']}")
                    print(f"Data de Lançamento: {episode['data_registro']}")
                    novo_ep = True
                    dowload = ler_dowloads()
                    heder = {'Referer': 'https://www.anroll.net/'}
                    bJson = requests.get(f"https://cdn-zenitsu-gamabunta.b-cdn.net/cf/hls/animes/{episode['anime']['slug_serie']}/{episode['n_episodio']}.mp4/media-1/stream.m3u8", headers=heder)
                    if bJson.status_code == 200:
                        data = bJson.text
                        id = str(uuid.uuid4())
                        caminho = '/tmp/' + id + '.m3u8'
                        caminho_mp4 = '/tmp/' + id + '.mp4'
                        with open(caminho, 'w') as file:
                            file.write(data)
                        comando_ffmpeg = ["ffmpeg", "-protocol_whitelist", "file,https,tcp,tls,crypto", "-i", caminho, "-c", "copy", caminho_mp4]
                        subprocess.run(comando_ffmpeg)
                        for dowload in dowloa:
                            if dowloa["anime"] == anime["nome"] and dowloa["episodio"] == episode['n_episodio']:
                                dowloa.remove(dowloa)
                        dowload.append({"id": id, "anime": anime["nome"], "episodio": episode['n_episodio'], "titulo": episode['titulo_episodio'], "caminho": caminho_mp4})
                        escrever_dowloads(dowload)
                    else:
                        print("falha no dowload")
        else:
            print("##############################")
            print("Falha na requisição")
            print("##############################")

def listar_dowloads():
    dowloads = ler_dowloads()
    for dowload in dowloads:
        print(dowload["id"])
        print(dowload["anime"])
        print(dowload["episodio"])
        print(dowload["titulo"])
        print("********************")
    print("digite o id do dowload")
    id = input()
    for dowload in dowloads:
        if dowload["id"] == id:
            print("deseja assistir? 1 - sim, 2 - nao")
            opcao = int(input())
            if opcao == 1:
                subprocess.run(["vlc", dowload["caminho"]])
                store = ler_dados()
                for anime in store:
                    if anime["nome"] == dowload["anime"]:
                        anime["ultimo_episodio"] = int(dowload["episodio"])
                        escrever_dados(store)
                        dowloads.remove(dowload)
                        escrever_dowloads(dowloads)
            else:
                print("dowload nao assistido")
            break