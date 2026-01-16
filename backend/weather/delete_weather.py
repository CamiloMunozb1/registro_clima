# Importacion de librerias necesarias para la creacion del Blueprint y la importacion de la base de datos.
from flask import Blueprint,request,jsonify
from backend.data import conexion
from dotenv import load_dotenv
from psycopg2 import InternalError,DatabaseError,IntegrityError

# Creacion del Blueprint para usarla como funcion modular de la aplicacion.
delete_wheather = Blueprint('delete','__name__')
load_dotenv() # Carga de las variables de entorno.

def conexion_db():
    return conexion.conexion_db() # Retorno de la conexion con la base de datos.

# Enrutador del blueprint para la eliminacion de un registro, con el metodo POST para pasarlo a la base de datos.
@delete_wheather.route('/delete',methods=['POST'])
def delete_weather():
    data = request.get_json() # Conversion de la informacion pasada a un archivo Json.
    try:

        city_id = int(data.get('city_id','')) # Se pasa el id de la ciudad.
        register_id = int(data.get('register_id','')) # Se pasa el id del registro.
        # Validador de campo.
        if not all([city_id,register_id]):
            return jsonify({'Error' : 'el campo debe estar completo para la eliminacion.'}),400
    # Manejo de errores.
    except ValueError:
        return jsonify({'Error' : 'el tipo de dato no es el solicitado.'}),400
    
    conn = conexion_db() # Se toma la conexion con la base de datos.
    if conn is None: # Validador por si no se encuentra la conexion con la base de datos.
        return jsonify({'Error' : 'no se encontro la conexion con la base de datos.'})
    
    try:
        cursor = conn.cursor() # Creacion del cursor para el manejo con la base de datos.
        # Se usa esta consulta para validar si se encuentra el id de la ciudad.
        cursor.execute('''SELECT * view_clima WHERE city_id = %s''',(city_id))
        if cursor.fetchone() is None:
            return jsonify({'Error' : 'no se encontro el id seleccionado.'}),400
        # Se hace una elimiacion en cascada para eliminar el id de la ciudad y esta misma en el registro.
        cursor.execute('''DELETE FROM view_clima WHERE city_id = %s''',(city_id))
        cursor.execute('''DELETE FROM registro_clima WHERE city_id = %s''',(register_id))
        if cursor.rowcount == 0: # Se verifica si el ID se encuentra junto con el registro.
            return jsonify({'Error' : 'no se encontro el id de la ciudad en el registo.'}),400
        conn.commit() # Subida de cambios a la base de datos.
        return jsonify({'Mensaje' : 'los datos se borraron del registro.'}),200
    # Manejo de errores.
    except InternalError:
        conn.rollback() # Se revierten los cambios de la base de datos.
        return jsonify({'Error' : 'erroor interno en la base de datos.'}),400
    except DatabaseError:
        conn.rollback() # Se revierten los cambios de la base de datos.
        return jsonify({'Error' : 'error en la base de datos.'}),400
    except IntegrityError:
        conn.rollback() # Se revierten los cambios de la base de datos.
        return jsonify({'Error' : 'error de integridad en la base de datos.'}),400
    except Exception as error:
        return jsonify({'Error' : f'error inesperado en el programa : {str(error)}.'}),400
    finally:
        cursor.close() # Cierre del cursor.
        conn.close() # Cierre de la conexion.
    
