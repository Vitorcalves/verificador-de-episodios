#!/usr/bin/env python

from operacoes_anime import adicionar_anime, remover_anime, verificar_ep, lista_ep, dowload_ep, editar_anime, lista_ep_anime, listar_dowloads
from db import printar_banco


def opcoes():
    print("opcoes:")
    print("1 - adicionar anime")
    print("2 - remover anime")
    print("3 - verificar novos episodios")
    print("4 - lista episodios")
    print("5 - baixar episodio")
    print("6 - editar ep")
    print("7 - printar banco")
    print("8 - lista todos episodios anime")
    print("9 - visualizar dowloads")
    print("0 - sair")



# Chama a função
opcoes()
opcao = int(input("opcao: "))
while opcao != 0:
    if opcao == 1:
        adicionar_anime()
    elif opcao == 2:
        remover_anime()
    elif opcao == 3:
        verificar_ep()
    elif opcao == 4:
        lista_ep()
    elif opcao == 5:
        dowload_ep()
    elif opcao == 6:
        editar_anime()
    elif opcao == 7:
        printar_banco()
    elif opcao == 8:
        lista_ep_anime()
    elif opcao == 9:
        listar_dowloads()
    else:
        print("opcao invalida")
    opcoes()
    opcao = int(input("opcao: "))

