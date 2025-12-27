## Registro del clima
Este es un proyecto Backend con formato RESTfull desarrollado con Flask para el ingreso, gestion y busqueda de registros del clima.
Donde se busca una dvision de aplicaciones para: ingreso y seguimiento del clima con una base de datos local en PostgreSQL. Donde la
API nos ayuda a gestionar un registro del clima mas especifico para su ingreso a la base de datos.

## Caracteristicas principales
-API REST con Flask: se gestionan los enrutadores para ingreso, registro, eliminacion y visualización de la informacion pasada por el usuario y la informacion dada por la API.

-Conexion con PostegreSQL: persistencia de los datos de manera local.

-Uso de la API: registro constante de la informacion del clima para consultar y plasmarla en la base de datos.

## Requisitos:
-Python 3.x

-PostgreSQL (Acceso a tu base de datos).

-Acceso a la API (Token de integracion).

-Dependencias de Python, las principales librerias usadas en este proyecto se usa pip:
       pip install Flask flask-cors psycopg2-binary python-dotenv requests

## Configuracion del entorno
La aplicacion configuro variables de entorno para el manejo de credenciales (con informacion de la base de datos y la API). Debes crear un archivo .env en la raiz del proyecto.

            # ------------------------------------
            # CONFIGURACIÓN DE POSTGRESQL
            # ------------------------------------
            DB_HOST=localhost
            DB_NAME=mis_peliculas
            DB_USER=postgres
            DB_PASSWORD=mysecretpassword
            DB_PORT=5432
          
            # ------------------------------------
            # CONFIGURACIÓN DE LA API
            # ------------------------------------
            # El Token de Integración de la API de Notion
            API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxx 


## Autor
Proyecto realizado por Juan Camilo Muñoz.

## Licencia
Este proyecto esta bajo una licencia MIT.
