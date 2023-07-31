############ EJECUTA QUERY #############
########################################
def ejecutaQuery(cnx_pool, query, parametros):

# Ejecuta query tomando una conexión del pool de conexiones,
# Luego convierte la lista pasada de parametros como una tupla
# Ejecuta el query 
# SELECT: Retorna una lista de registros.  Cada registro es una lista de valores de cada campo.
# INSERT: Retorna el último ID
# UPDATE/DELETE:  Retorna ['ok']

# consigue una conexión del pool

    # print('ENTRA a: ejecutaQuery')

    # quitamos espacios en blanco antes del comando
    query = query.strip()

    # print(' query y parametros:',query, parametros)


    cnx = cnx_pool.get_connection()
    cursor = cnx.cursor()

    # La ejecuta y salva el resultado en la variable registros
    # print('query:',query, "parametros:",parametros)
    cursor.execute(query, tuple(parametros))

    # este es el comando incluido el reemplazo de parámetros
    comando_a_ejecutar = cursor.statement
    # print('comando a ejecutar: ', comando_a_ejecutar)

    # obtenemos el comando que se ejecutó
    comando = query[:6]
    comando = comando.upper()

    registros = []

    if comando == 'SELECT':
        registros = cursor.fetchall()
        # print('regsitros:', registros)
    else:
        cnx.commit()

    if comando == 'INSERT' or comando == 'UPDATE':
        query_last_id = "SELECT LAST_INSERT_ID()"
        cursor.execute(query_last_id)
        last_id = cursor.fetchone()[0]
        registros = last_id

    # cierra la conexión del pool
    cursor.close()
    cnx.close()

    return(registros)

