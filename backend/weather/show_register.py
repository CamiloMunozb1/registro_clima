# Importacion de librerias para crear el Blueprint y la importacion de la base de datos.
from flask import Blueprint,request,jsonify
from backend.data import conexion
from dotenv import load_dotenv
from psycopg2 import InternalError,DatabaseError,IntegrityError
import pandas as pd # Uso de pandas para la lectura de datos.

# Creacion del Blueprint para usarla como funcion modular de la aplicacion.
show_register = Blueprint('mostar_registros','__name__')
load_dotenv()

def conexion_db():
    return conexion.conexion_db() # Retorno de la conexion con la base de datos.

# Enrutador del Blueprint para la muestra de datos, con el metodo GET para traer los datos registrados.
@show_register.route('/mostrar',methods=['GET'])
def show_register():
    data = request.get_json() # Se convierte la informacion solicitada a uun formato Json.
    city_id = int(data.get('city_id','')) # Entrada del ID de la ciudad.
    if not city_id: # Validador de campo.
        return jsonify({'Error' : 'el campo no puede estar vacio.'}),400
    try:
        conn = conexion_db() # Se toma la conexion con la base de datos.
        if conn is None: # Condicion por si no se encuenta la conexion con la base de datos.
            return jsonify({'Error' : 'no se encontro la conexion con la base de datos.'}),400
        
        cursor = conn.cursor() # Creacion del cursor para el manejo de la base de datos.
        # Se hace esta consulta para identificar el ID ingresado.
        cursor.execute('''SELECT * FROM view_clima WHERE city_id = %s''',(city_id,))
        if cursor.fetchone() is None: # Validador de campo.
            return jsonify({'Error' : 'ID de la ciudad no encontrado'}),400
        '''
            Consulta a la base de datos donde juntamos las tablas View_clima y registro clima
            Esto con el fin de mostrar los registros usando el ID de la ciudad como key foranea
            los registros se ordendan de manera descendente
        '''
        query = pd.read_sql_query('''
                        SELECT register_id,meteorological_phenomena,meteorological_parameters
                        FROM registro_clima
                        INNER JOIN
                        view_clima ON registro_clima.city_id = view_clima.city_id
                        WHERE
                        city_id = %s
                        ORDER BY
                        register_id DESC
                    ''',conn,params=[city_id])
        resultado = query.to_dict(['records']) # Pasamos el resultado a un diccionario.
        if not resultado: # Condicion por si no se encuentran registros
            return jsonify({'Mensaje' : 'no se encontraron registos'}),200
        else:
            return jsonify({'Mensaje' : f'{resultado}'}),200
    # Manejo de errores.
    except InternalError:
        return jsonify({'Error' : 'error interno en la base de datos.'}),400
    except DatabaseError:
        return jsonify({'Error' : 'error inesperado en la base de datos'}),400
    except IntegrityError:
        return jsonify({'Error' : 'error de integridad en la base de datos.'}),400
    except Exception as error:
        return jsonify({'Error' : f'error inesperado en el programa : {str(error)}'}),400
    finally:
        cursor.close() # Cierre del cursor.
        conn.close() # Cierre de la conexion.