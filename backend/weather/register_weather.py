# Importacion de las librerias necesarias para la creacion del Blueprint y la importacion de la base de datos.
from flask import Blueprint,request,jsonify
from backend.data import conexion
from dotenv import load_dotenv
from psycopg2 import InternalError,DatabaseError,IntegrityError

# Creacion del Blueprint para usarla como funcion modular de la aplicacion.
register_weather = Blueprint('register','__name__')
load_dotenv() # Carga de las variables de entorno.

def conexion_db():
    return conexion.conexion_db() # Retorno de la copnexion con la base de datos.

# Enrutador modular del Blueprint con el metodo 'POST' para subir la informacion a la base de datos.
@register_weather.route('/register',methods = ['POST'])
def register_wearher():
    data = request.get_json() # Convierte la informacion a un formato Json.

    try:
        # Ingreso de usuario.
        city_id = int(data.get('city_id',''))
        meteorological_phenomena = str(data.get('fenomenos_metereologicos','')).strip()
        meteorological_parameters = str(data.get('parametros_metereologicos','')).strip()
        # Validador de campos.
        if not all[(city_id,meteorological_phenomena,meteorological_parameters)]:
            return jsonify({'Error' : 'todos los parametros deben estar completos'}),400
    # Manejo de error.
    except ValueError:
        return jsonify({'Error' : 'el tipo de dato no es el solicitado, por favor volver a digitar'}),400
    
    conn = conexion_db() # Se toma la conexion con la base de datos.
    if conn is None: # Validador por si no se encuentra la conexion.
        return jsonify({'Error' : 'no se encontro la conexion con la base de datos.'}),400
    
    try:
        cursor = conn.cursor() # Creacion del cursor para el manejo con la base de datos.
        # Consulta a la base de datos para la subida de la informacion meteorologica registrada.
        cursor.execute('''
                        INSERT INTO 
                        registro_clima(meteorological_phenomena,meteorological_parameters,city_id) 
                        VALUES (%s,%s,%s,%s)''',(meteorological_phenomena,meteorological_parameters,city_id))
        conn.commit() # Subida de la informacion a la base de datos.
        return jsonify({'Mensaje' : 'informacion subida con exito'}),200
    # Manejo de errores.
    except InternalError:
        conn.rollback()
        return jsonify({'Error' : 'error interno en la base de datos.'}),400
    except DatabaseError:
        conn.rollback()
        return jsonify({'Error' : 'error en la base de datos.'}),400
    except IntegrityError:
        conn.rollback()
        return jsonify({'Error' : 'error de integridad en la base de datos.'}),400
    except Exception as error:
        return jsonify({'Error' : f'error inesperado en el programa : {str(error)}.'}),400 
    finally:
        cursor.close() # Cierre del cursor.
        conn.close() # Cierre de la conexion.
