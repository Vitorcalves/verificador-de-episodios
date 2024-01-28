import requests
import json

def verificar_novos_episodios():
    url = "https://apiv3-prd.anroll.net/animes/1522/episodes?page=1&order=desc"
    response = requests.get(url)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        data = response.json()

        # Itera sobre os episódios e imprime as informações
        for episode in data['data']:
            print(f"Episódio {episode['n_episodio']}: {episode['titulo_episodio']}")
            print(f"Data de Lançamento: {episode['data_registro']}")
            print("---")
    else:
        print("Falha na requisição")

def adicionar_anime():
    print("adicionar anime")
    store = ler_dados()
    print("digite o nome do anime")
    nome = input()
    print("digite link da API")
    api = input()
    print("digite o link do anime")
    link = input()
    print("digite o numero do ultimo episodio ou deixe em branco e sera considerado 0")
    ultimo_episodio = input()
    if ultimo_episodio == "":
        ultimo_episodio = 0
    else:
        ultimo_episodio = int(ultimo_episodio)
    id = len(store)
    store.append({"id":id, "nome": nome, "api": api, "link": link, "ultimo_episodio": ultimo_episodio})
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
                    print("deseja atualizar o ultimo episodio? 1 - sim,  2 - nao, 3 - parar")
                    opcao = int(input())
                    if opcao == 1:
                        anime["ultimo_episodio"] = int(episode['n_episodio'])
                        escrever_dados(store)
                    elif opcao == 3:
                        continuar_verificacao = False
                        break
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
    

def printar_dados():
    store = ler_dados()
    for anime in store:
        print(anime["id"], anime["nome"],anime["ultimo_episodio"])
    
def printar_banco():
    store = ler_dados()
    for anime in store:
        print(anime["id"], anime["nome"],anime["ultimo_episodio"], anime["api"], anime["link"])  

def escrever_dados(store):
    with open('store.json', 'w') as file:
        json.dump(store, file)

def escrever_delete( dado ):
    deletados = ler_delete()
    deletados.append(dado)
    with open('delete.json', 'w') as file:
        json.dump(deletados, file)

def ler_delete():
    with open('delete.json', 'r') as file:
        dados = json.load(file)
        return dados

def ler_dados():
    with open('store.json', 'r') as file:
        dados = json.load(file)
        return dados

def opcoes():
    print("opcoes:")
    print("1 - adicionar anime")
    print("2 - remover anime")
    print("3 - verificar novos episodios")
    print("4 - lista episodios")
    print("5 - editar ep")
    print("6 - printar banco")
    print("7 - sair")


# Chama a função
opcoes()
opcao = int(input("opcao: "))
while opcao != 7:
    if opcao == 1:
        adicionar_anime()
    elif opcao == 2:
        remover_anime()
    elif opcao == 3:
        verificar_ep()
    elif opcao == 4:
        lista_ep()
    elif opcao == 5:
        editar_anime()
    elif opcao == 6:
        printar_banco()
    else:
        print("opcao invalida")
    opcoes()
    opcao = int(input("opcao: "))

