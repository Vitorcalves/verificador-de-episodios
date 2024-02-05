import json
def ler_dowloads():
       with open('/home/vitor/ads/teste_py/dowloads.json', 'r') as file:
        dados = json.load(file)
        return dados 

def escrever_dowloads(store):
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