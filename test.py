import time
import sys

def move_cursor_up(lines):
    print(f"\033[{lines}A", end='')  # Move o cursor 'lines' linhas para cima

def clear_line():
    print("\033[2K", end='')  # Limpa a linha na posição atual do cursor

def update_progress(download_id, progress):
    move_cursor_up(download_id + 1)  # +1 porque a contagem começa do zero
    clear_line()
    print(f"Download {download_id}: Progresso {progress}%")
    move_cursor_down(download_id + 1)  # Move para baixo para voltar à posição inicial

def move_cursor_down(lines):
    print(f"\033[{lines}B", end='')  # Move o cursor 'lines' linhas para baixo

# Simulação de atualização de progresso
download_count = 7  # Número total de downloads
# Inicialmente, move o cursor para baixo para criar espaço
for i in range(download_count):
    print()

for i in range(101):
    for download_id in range(download_count):
        update_progress(download_id, i)
    time.sleep(0.1)  # Espera um pouco antes da próxima atualização

# Limpa as linhas após a conclusão
for download_id in range(download_count):
    move_cursor_up(1)
    clear_line()