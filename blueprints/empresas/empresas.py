
import math
from flask import Blueprint, render_template, redirect, session, url_for
import appLib

from mysql.connector import pooling

empresas_bp = Blueprint("empresas", __name__, template_folder="templates")

config = {
    'charset': 'utf8',
    'init_command': 'SET SESSION lc_time_names = "es_ES";'
}

cnx_pool = pooling.MySQLConnectionPool(pool_name="mailTracker_pool_empresas",
                                        pool_size=20,
                                        pool_reset_session=True,
                                        host='localhost',
                                        database='mailtracker',
                                        user='mailtracker',
                                        password='mt',
                                        **config
                                      )
filtro = ''
pagina_actual = 1
registros_x_pagina = 3

query_select = ''
query_where = ''
query_order = ''
query = ''

limit = 0   # cuantas filas mostrar
offset = 0  # cuantas filas deja pasar

# si estamos en  página_actual= 1, y cada página es de 10 registros, regitros_x_pagina = 10,  entonces
# limit = registros_x_pagina
# offset = (pagina_actual - 1)*registro_x_pagina

@empresas_bp.route("/inicio")
def inicio():
    
    print('inicio()')

    pagina_actual = 1

    query_select = """ 
        select e.id, e.nombre
        from empresa e 
        """
    query_where = ''
    query_order = 'order by e.id'

    cantidad_registros = (pagina_actual-1)*registros_x_pagina
    query = query_select + query_where + query_order + ' limit ' + str(registros_x_pagina) + ' offset ' + str(cantidad_registros)

    session['pagina_actual'] = pagina_actual

    session['query_select'] = query_select
    session['query_where'] = query_where
    session['query_order'] = query_order

    # registros = consulta()
      
    return redirect(url_for('empresas.consulta'))

@empresas_bp.route("/consulta")
def consulta():
    
    print('consulta()')

    pagina_actual = session['pagina_actual']
    query_select = session['query_select']
    query_where = session['query_where']
    query_order = session['query_order']

    cantidad_registros = (pagina_actual-1)*registros_x_pagina
    query = query_select + query_where + query_order + ' limit ' + str(registros_x_pagina) + ' offset ' + str(cantidad_registros)

    print('query:',query)

    empresas = appLib.ejecutaQuery(cnx_pool, query, [])
    print(empresas)

    return empresas

@empresas_bp.route("/siguiente")
def siguiente():
    
    print('siguiente()')

    pagina_actual = session['pagina_actual']
    query_select = session['query_select']
    query_where = session['query_where']
    query_order = session['query_order']

    # vamos a mirar cuántas páginas tiene este query sin limit y sin offset
    query = query_select + query_where + query_order

    registros = appLib.ejecutaQuery(cnx_pool, query, [])
    total_registros = len(registros)
    total_paginas = math.ceil(total_registros / registros_x_pagina)  # // da la parte entera

    # solo aumentamos la página actual, si el query tiene toda esa cantidad de páginas
    if pagina_actual + 1 <= total_paginas:
        pagina_actual = pagina_actual + 1

    session['pagina_actual'] = pagina_actual
    print('pagina actual:', pagina_actual)

    return redirect(url_for('empresas.consulta'))

@empresas_bp.route("/ultima")
def ultima():
    
    print('ultima()')

    pagina_actual = session['pagina_actual']
    query_select = session['query_select']
    query_where = session['query_where']
    query_order = session['query_order']

    # vamos a mirar cuántas páginas tiene este query sin limit y sin offset
    query = query_select + query_where + query_order

    registros = appLib.ejecutaQuery(cnx_pool, query, [])
    total_registros = len(registros)
    pagina_actual = math.ceil(total_registros / registros_x_pagina)  # vamos a la última pagina
    session['pagina_actual'] = pagina_actual
    print('pagina actual:', pagina_actual)

    return redirect(url_for('empresas.consulta'))

@empresas_bp.route("/anterior")
def anterior():
    
    print('anterior()')

    pagina_actual = session['pagina_actual']


    # solo reducimos la página actual, si aún no hemos llegado a la página 1
    if pagina_actual - 1 >= 1:
        pagina_actual = pagina_actual - 1

    session['pagina_actual'] = pagina_actual
    print('pagina actual:', pagina_actual)

    return redirect(url_for('empresas.consulta'))

@empresas_bp.route("/primera")
def primera():
    
    print('primera()')

    pagina_actual = 1

    session['pagina_actual'] = pagina_actual
    print('pagina actual:', pagina_actual)

    return redirect(url_for('empresas.consulta'))





