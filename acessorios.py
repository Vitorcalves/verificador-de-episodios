def migrar_db():
    store = ler_dados()
    for anime in store:
        conexao = conectar_db()
        if conexao == None:
            print("falha na conexao")
            return
        with conexao:
            with conexao.cursor() as cursor:
                cursor.execute("INSERT INTO anime (name_anime, ultimo_ep, plataforma, id_externo, slug_serie) VALUES (%s, %s, %s, %s, %s)", (anime["nome"], anime["ultimo_episodio"], 1, anime["id_externo"], anime["slug"]))
        conexao.close()
    print("migracao concluida")

def apagar_animes():
    id_inicial = 6
    id_final = 10
    conexao = conectar_db()
    if conexao is None:
        print("Falha na conexão")
        return
    with conexao:
        with conexao.cursor() as cursor:
            try:
                # Construa e execute a instrução SQL para deletar as linhas
                cursor.execute(
                    "DELETE FROM anime WHERE id_anime >= %s AND id_anime <= %s",
                    (id_inicial, id_final)
                )
                print("Animes apagados com sucesso.")
            except Exception as e:
                print(f"Ocorreu um erro ao apagar animes: {e}")
    conexao.close()

def apagar_dowloads(id_dowloads):
    conexao = conectar_db()
    if conexao is None:
        print("Falha no banco")
        return
    with conexao:
        with conexao.cursor() as cursor:
            try:
                os.remove(f'/home/vitor/dowloads_animes/{id_dowloads}.mp4')
            except Exception as e:
                print(f"Ocorreu um erro ao apagar o arquivo: {e}")
            try:
                cursor.execute("DELETE FROM dowloads WHERE id_dowloads = %s", (id_dowloads,))
            except Exception as e:
                print(f"Ocorreu um erro ao apagar registro no db: {e}")
    conexao.close()

def printar_banco_db():
    conexao = conectar_db()
    if conexao is None:
        print("Falha na conexão com o banco")
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM anime JOIN plataforma ON anime.plataforma = plataforma.id_plataforma WHERE ativo = true")
            animes = cursor.fetchall()
            for anime in animes:
                print(f"ID: {anime['id_anime']}, Nome: {anime['name_anime']}, Ultimo Episodio: {anime['ultimo_ep']}, Plataforma: {anime['name_plataforma']}")
    conexao.close()

def criar_backup():
    conexao = conectar_db()
    if conexao is None:
        print("Falha na conexão")
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                # Construa e execute a instrução SQL para deletar as linhas
                cursor.execute(
                    "SELECT * FROM anime JOIN plataforma ON anime.plataforma = plataforma.id_plataforma WHERE ativo = true"
                )
                animes = cursor.fetchall()
                stor=[]
                for anime in animes:
                    stor.append({
                        "id": anime["id_anime"],
                        "nome": anime["name_anime"],
                        "ultimo_episodio": anime["ultimo_ep"],
                        "api": anime["link_api"],
                        "link": anime["link_plataforma"],
                        "download": anime["link_dowloads"],
                        "id_externo": anime["id_externo"],
                        "slug": anime["slug_serie"]
                    })
                print(stor)
                escrever_dados(stor)
                print("Backup criado com sucesso.")
            except Exception as e:
                print(f"Ocorreu um erro ao criar o backup: {e}")
    conexao.close()
