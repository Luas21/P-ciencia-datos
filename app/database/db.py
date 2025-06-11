import psycopg2
from psycopg2 import DatabaseError
from decouple import config

#parámetros establecidos en .env para realizar la conexión a la BD
def get_connection():
    try:
        return psycopg2.connect(
            host=config('DB_HOST'),
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            database=config('DB_NAME'),
            port=config('DB_PORT')
        ) 
    except DatabaseError as ex:
        raise ex