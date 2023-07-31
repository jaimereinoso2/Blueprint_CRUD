# demo de cómo usar blueprint correctamente con flask y usar esa funcionalidad para permitir
# CRUD sobre dos tablas distintas

from flask import Flask

# aqui se definen los blueprints que vamos a registrar
from blueprints.helloword.helloword import helloword
from blueprints.bye.bye import bye

# MYSQL y sus configuraciones
from mysql.connector import Error
from mysql.connector import pooling
import appLib

config = {
    'charset': 'utf8',
    'init_command': 'SET SESSION lc_time_names = "es_ES";'
}

print('...  iniciando pool de conexiones ..')
cnx_pool = pooling.MySQLConnectionPool(pool_name="mailTracker_pool",
                                        pool_size=20,
                                        pool_reset_session=True,
                                        host='localhost',
                                        database='mailtracker',
                                        user='mailtracker',
                                        password='mt',
                                        **config
                                      )


departamentos = appLib.ejecutaQuery(cnx_pool, 
            """ 
            select  d.id, d.nombre, e.id, e.nombre
            from departamento d
            inner join empresa e
            on e.id = d.empresa_id
            """, [])

print(departamentos)

app = Flask(__name__)

# En esta sección se registran los blueprints
app.register_blueprint(helloword)
app.register_blueprint(bye, url_prefix="/bye")




if __name__ == "__main__":
    app.run(port=50005, debug=True)
        


