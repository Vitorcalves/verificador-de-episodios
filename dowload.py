from db import conectar_db, listar_todos_dowloads
from psycopg2.extras import RealDictCursor
import requests
import uuid
import subprocess
import os
import threading
import re
import sys

def dowload_ep_db(name_anime ,link_dowload, id_anime, numero_ep, titulo_ep, callback_progresso=None):
    try:
        heder = {'Referer': 'https://www.anroll.net/'}
        
        bJson = requests.get(link_dowload, headers=heder)
        if bJson.status_code == 200:
            
            data = bJson.text
            id = str(uuid.uuid4())
            caminho = '/tmp/' + id + '.m3u8'
            caminho_mp4 = '/home/vitor/dowloads_animes/' + id + '.mp4'
            with open(caminho, 'w') as file:
                file.write(data)
            
            comando_ffmpeg = ["ffmpeg", "-protocol_whitelist", "file,https,tcp,tls,crypto", "-i", caminho, "-c", "copy", caminho_mp4]
            processo = subprocess.Popen(comando_ffmpeg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            
            while True:
                output = processo.stderr.readline()
                
                if output == '' and processo.poll() is not None:
                    break
                elif callback_progresso:
                    callback_progresso(name_anime ,id_anime, numero_ep, output)
            
            rc = processo.poll()
            conexao = conectar_db()
            if conexao == None:
                print('falha na conexao com banco')
                return
            with conexao:
                with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute('SELECT * FROM dowloads WHERE id_anime = %s AND numero_ep = %s', (id_anime, numero_ep)) 
                    dowload = cursor.fetchall()
                    if len(dowload) > 0:
                        cursor.execute('DELETE FROM dowloads WHERE id_anime = %s AND numero_ep = %s', (id_anime, numero_ep))
                        cursor.execute('INSERT INTO dowloads (id_anime, numero_ep, titulo_ep, id_dowloads) VALUES (%s, %s, %s, %s)', (id_anime, numero_ep, titulo_ep, id))
                    else:
                        cursor.execute('INSERT INTO dowloads (id_anime, numero_ep, titulo_ep, id_dowloads) VALUES (%s, %s, %s, %s)', (id_anime, numero_ep, titulo_ep, id))
            conexao.close()
        else:
            print('falha no dowload: status code diferente de 200')
    except Exception as e:
        print(f'falha no dowload try: {e}')

def dowloads_asincronos(dowloads):
    threads = []
    display = {}

    def printa_progresso():
        print("\033c", end='')  # Cuidado: isso limpa a tela.
        for key, value in display.items():
            print(f'Anime {value["name"]} Episódio {value["numero_ep"]} - {value["andamento"]:.2f}% completo')

    def atualiza_progresso(name, id_anime, numero_ep, progresso):
        duracao_video_match = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2})\.\d{2},', progresso)
        if duracao_video_match:
            horas = int(duracao_video_match.group(1))
            minutos = int(duracao_video_match.group(2))
            segundos = int(duracao_video_match.group(3))
            duracao_total_segundos = (horas * 3600) + (minutos * 60) + segundos
            display[str(id_anime) + numero_ep]= {'duracao': duracao_total_segundos, 'andamento': 0, 'name': name, 'numero_ep': numero_ep}

        tempo_match = re.search(r'time=(\d{2}):(\d{2}):(\d{2})\.\d{2}', progresso)
        if tempo_match:
            horas = int(tempo_match.group(1))
            minutos = int(tempo_match.group(2))
            segundos = int(tempo_match.group(3))
            duracao_total_segundos = (horas * 3600) + (minutos * 60) + segundos
            display[str(id_anime)+numero_ep]['andamento']= duracao_total_segundos / display[str(id_anime)+numero_ep]['duracao'] * 100
            printa_progresso()


    dowloads_db = listar_todos_dowloads()

    if len(dowloads_db) > 0:
        for dowload in dowloads_db:
            for ep in dowloads:
                if dowload['id_anime'] == ep['id_anime'] and dowload['numero_ep'] == ep['numero_ep']:
                    dowloads.remove(ep)
                    break
    if len(dowloads) == 0:
        return
    
    for episodio in dowloads:
        thread = threading.Thread(target=dowload_ep_db, args=(episodio['name_anime'] ,episodio['link_dowload'], episodio['id_anime'], episodio['numero_ep'], episodio['titulo'], atualiza_progresso))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()            

def dowload_novos_ep_db():
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute('SELECT * FROM anime a JOIN plataforma p ON a.plataforma = p.id_plataforma WHERE a.ativo = true')
            animes = cursor.fetchall()
            ep_dowload = []
            for anime in animes:
                url_api = anime['link_api'].replace('{id_externo}', str(anime['id_externo']))
                response = requests.get(url_api)
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
                            print('---')
                            ep_dowload.append({'link_dowload': anime['link_dowloads'].replace("{'slug_serie'}", anime['slug_serie']).replace("{'n_episodio'}", episode['n_episodio']), 'id_anime': anime['id_anime'], 'numero_ep': episode['n_episodio'], 'titulo': episode['titulo_episodio'], 'name_anime': anime['name_anime']})
                else:
                    print('##############################')
                    print('Falha na requisição')
                    print('##############################')
            if len(ep_dowload) > 0:
                dowloads_asincronos(ep_dowload)
                subprocess.run(['stty', 'sane'])
                print('dowloads realizados')
    conexao.close()
