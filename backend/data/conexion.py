# Importacion de librerias para la conexion con la base de datos.
from flask import Flask,jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from psycopg2 import InternalError,DatabaseError,IntegrityError
import psycopg2
import os

# Creacion de una aplicacion flask
app = Flask(__name__)
# Conexion con el Fronted de la aplicacion.
CORS(app,origins='www.paginaejemplo.com',supports_credentials=True)
load_dotenv() # Carga de las variables de entorno

# Funcion para conectar la base de datos.
def conexion_db():
    try:
        # Uso de las variables de entorno para conectar con la base de datos.
        conn = psycopg2.connect(
            host = os.getenv('DB_HOST'),
            dbname = os.gentenv('DB_NAME'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            port = os.getenv('DB_PORT'),
            sslmode = os.getenv('DB_SSL')
            )
        return conn # Retorno de la conexion.
    # Manejo de errores.
    except InternalError:
        return jsonify({'Error' : 'error interno en la base '}),400
    except DatabaseError:
        return jsonify({'Error' : 'error inesperado en la base de datos.'}),400
    except IntegrityError:
        return jsonify({'Error' : 'error de integridad en la base de datos.'}),400
    except Exception as error:
        return jsonify({'Error' : f'error inesperado : {str(error)}'}),400
