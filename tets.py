#!/usr/bin/env python

from operacoes_anime import  adicionar_anime_db, remover_anime_db, listar_ep_anime_db, dowload_novos_ep_db, listar_dowloads_db, verificar_ep_db, listar_novos_ep_db, editar_anime_db
from db import printar_banco


def opcoes():
    print("opcoes:")
    print("1 - adicionar anime")
    print("2 - remover anime")
    print("3 - verificar novos episodios")
    print("4 - lista episodios")
    print("5 - baixar episodio")
    print("6 - editar ep")
    print("7 - lista todos episodios anime")
    print("8 - visualizar dowloads")
    print("0 - sair")



# Chama a função

opcoes()
opcao = int(input("opcao: "))
while opcao != 0:
    if opcao == 1:
        adicionar_anime_db()
    elif opcao == 2:
        remover_anime_db()
    elif opcao == 3:
        verificar_ep_db()
    elif opcao == 4:
        listar_novos_ep_db()
    elif opcao == 5:
        dowload_novos_ep_db()
    elif opcao == 6:
        editar_anime_db()
    elif opcao == 7:
        listar_ep_anime_db()
    elif opcao == 8:
        listar_dowloads_db()
    else:
        print("opcao invalida")
    opcoes()
    opcao = int(input("opcao: "))

