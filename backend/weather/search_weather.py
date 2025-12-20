# Importacion de las librerias necesarias para la aplicacion y las funciones modulares para la aplicacion.
from flask import Flask,request,jsonify
from backend.data import conexion
from backend.weather import register_weather
from backend.weather import delete_weather
from backend.weather import show_register
from flask_cors import CORS
from dotenv import load_dotenv
from psycopg2 import InternalError,DatabaseError,IntegrityError
import requests
import os

# Creacion de la aplicacion flask.
app = Flask(__name__)
# Conexion con el Fronted de la aplicacion para el paso de la informacion.
CORS(app,origins='www.paginaejemplo.com',supports_credentials=True)
load_dotenv() # Carga de las variables de entorno.

# Paso de las funciones modulares de la aplicacion.
app.register_blueprint(register_weather)
app.register_blueprint(delete_weather)
app.register_blueprint(show_register)

# Uso de la conexion con la base de datos.
def conexion_db():
    return conexion.conexion_db() # Retorno de la conexion.

def clima_api(user_city): # La funcion de la API se le pasa como argumento la ciudad que ingresa el usuario. 
    try:
        api_key = os.getenv('API_KEY') # Variable de entorno que contiene la API_KEY
        # URL para buscar la informacion solicitada.
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={user_city}&limit=5&appid={api_key}'
        respuesta = requests.get(url) # Se hace la consulta HTTP y se guarda la informacion.
        if respuesta.status_code == 200: #Se revisa el estado de la peticion HTTP.
            data = respuesta.json() # Se convierte la respuesta a formato Json para su lectura.
            ubicacion = data[0]['name'] # Se toma la ubicacion del lugar.
            latitud = data[0]['lat'] # Se toma la latitud del lugar.
            longitud = data[0]['lon'] # Se toma la longitud del lugar.
            pais = data[0]['country'] # Se toma el pais del lugar.
            print(f'El nombre de la ciudad es : {ubicacion}')
            print(f'El pais al que corresponde la ciudad es: {pais}')
            # Segunda url para revisar los fenomenos meteorologicos.
            url_dos = f'https://api.openweathermap.org/data/2.5/weather?lat={latitud}&lon={longitud}&appid={api_key}&units=metric&lang=es'
            respuesta_dos = requests.get(url_dos) # Se realiza la peticion HTTP y se guarda la respuesta.
            if respuesta_dos.status_code == 200: # Estado de la peticion HTTP.
                data_dos = respuesta_dos.json() # Se convierte la respuesta a formato Json.
                timezone = data_dos['timezone'] # Se toma el tiempo de la zona.
                descripcion = data_dos['weather'][0]['description'] # Se toma la descripcion del clima.
                main = data_dos['weather'][0]['main'] # Finalmente se toma la informacion del clima. 
                print(f'Nombre de la zona horaria : {timezone}')
                print(f'Fenomenos meteorologicoa actuales : {descripcion}')
                print(f'Parametros meteorologicos : {main}')
            else:
                print(f'error de conexion : {respuesta_dos.status_code}') # revision de error de est6ado de la peticion HTTP.
        else:
            print(f'No se pudo conectar con la API : {respuesta.status_code}') # revision de error de est6ado de la peticion HTTP.
    # Manejo de errores.
    except Exception as error:
        return jsonify({'Error' : f'error inesperado en la API : {str(error)}'}),400

# Enrutador para el ingreso de ciudades con el metodo 'POST' para subir esta informacion a la base de datos.
@app.route('/search',methods = ['POST'])
def search_weather():
    data = request.get_json() # Convierte la entrada en un formato Json.
    try:
        # Ingreso de usuario.
        user_city = str(data.get('search_city','')).strip()
        if not user_city: # Validador de campo.
            return jsonify({'Error' : 'el campo debe estar completo'}),400
    # Manejo de error.
    except ValueError:
        return jsonify({'Error' : 'el tipo de dato no es el solicitado, por favor volver a digitar.'}),400
        
    conn = conexion_db() # Tomamos la conexion con la base de datos.
    if conn is None: # Validador por si no se encuentra la conexion.
        return jsonify({'Error' : 'no se encontro la conexion con la base de datos.'}),400
    try:
        cursor = conn.cursor() # Creacion del cursor para manejo de la base de datos.
        # Consulta para subir la informacion a la base de datos.
        cursor.execute('''
                        INSERT INTO 
                        view_clima(user_city) 
                        VALUES (%s) RETURNING ID''',
                        (user_city))
        city_id = cursor.fetchone()[0] # Se busca el id generador por consulta.
        conn.commit() # Se sube la informacion a la base de datos.
        search_city = clima_api(user_city) # Paso de la ciudad a la API para consultar el clima.
        # Validador por si falla el paso o la conexion con la API.
        if search_city:
            conn.rollback() # Se revierten los cambios.
            return jsonify({'Error' : f'no se pudo encontrar la conexion con la API.'}),400
        return jsonify({'Mensaje' : 'se subieron con exito los datos a la base de datos', 'ID' : f'{city_id}'}),200
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
        return jsonify({'Error' : f'error inesperado en la aplicacion : {str(error)}.'}),400
    finally:
        cursor.close() # Cierre del cursor.
        conn.close() # Cierre de la conexion.

