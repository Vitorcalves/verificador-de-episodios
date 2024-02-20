#!/usr/bin/env python

from operacoes_anime import  adicionar_anime_db, remover_anime_db, listar_ep_anime_db, dowload_novos_ep_db, listar_dowloads_db, verificar_ep_db, listar_novos_ep_db, editar_anime_db, criar_backup, printar_banco_db
from db import printar_banco


def opcoes():
    print("opcoes:")
    print("1 - Gerenciar animes")
    print("2 - verificar novos episodios")
    print("3 - lista episodios")
    print("4 - baixar episodio")
    print("5 - lista todos episodios anime")
    print("6 - visualizar dowloads")
    print("7 - criar backup")
    print("0 - sair")

def opcoes_gerenciar_animes():
    print("opcoes:")
    print("1 - adicionar anime")
    print("2 - remover anime")
    print("3 - editar anime")
    print("0 - voltar")

# Chama a função


def main():
    opcoes()
    opcao = int(input("opcao: "))
    while opcao != 0:
        if opcao == 1:
            gerenciar_animes()
            break
        elif opcao == 2:
            verificar_ep_db()
        elif opcao == 3:
            listar_novos_ep_db()
        elif opcao == 4:
            dowload_novos_ep_db()
        elif opcao == 5:
            listar_ep_anime_db()
        elif opcao == 6:
            listar_dowloads_db()
        elif opcao == 7:
            criar_backup()
        else:
            print("opcao invalida")
        opcoes()
        opcao = int(input("opcao: "))

def gerenciar_animes():
    opcao = 1
    while opcao != 0:
        printar_banco_db()
        opcoes_gerenciar_animes()
        opcao = int(input("opcao: "))
        if opcao == 1:
            adicionar_anime_db()
        elif opcao == 2:
            remover_anime_db()
        elif opcao == 3:
            editar_anime_db()
        elif opcao == 0:
            main()
            break   
        else:
            print("opcao invalida")
listar_novos_ep_db()
main()

