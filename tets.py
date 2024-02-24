#!/usr/bin/env python
from dowload import dowload_novos_ep_db
from acessorios import criar_backup, printar_banco_db
from operacoes_anime import  adicionar_anime, remover_anime_db, listar_ep_anime_db, listar_dowloads, verificar_ep_db, listar_novos_ep_db, editar_anime_db


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

def sair():
    print("Saindo ...")

def opcao_invalida():
    print("Opção inválida. Por favor, tente novamente.")

def main():
    opcoes()  # Exibe as opções

    opcao_map = {
        1: gerenciar_animes,
        2: verificar_ep_db,
        3: listar_novos_ep_db,
        4: dowload_novos_ep_db,
        5: listar_ep_anime_db,
        6: listar_dowloads,
        7: criar_backup,
        0: sair
    }

    try:
        opcao = int(input("opcao: "))
        # Obtém a função correspondente à opção escolhida ou opcao_invalida() se não encontrar
        acao = opcao_map.get(opcao, opcao_invalida)
        acao()  # Executa a função
        if opcao != 0:  # Se a opção não for sair, continua executando
            main()
    except ValueError:
        print("Opção inválida. Por favor, digite um número.")
        main()


def gerenciar_animes():
    printar_banco_db()
    opcoes_gerenciar_animes()

    opcao_map = {
        1: adicionar_anime,
        2: remover_anime_db,
        3: editar_anime_db,
        0: sair
    }

    try:
        opcao = int(input("opcao: "))
        acao = opcao_map.get(opcao, opcao_invalida)
        acao()
        if opcao != 0:
            gerenciar_animes()
    except ValueError:
        print("Opção inválida. Por favor, digite um número.")
        gerenciar_animes()

listar_novos_ep_db()
main()

