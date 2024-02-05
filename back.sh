#!/bin/bash

# Definir variáveis
CAMINHO_BANCO_DADOS="/home/vitor/senhas"
CAMINHO_BACKUP="senhas/"


# Fazer upload para o Google Drive
gdrive files upload "/home/vitor/senhas/Senhas.kdbx"
