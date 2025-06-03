import psycopg2
from psycopg2 import DatabaseError
#from decouple import config

#parámetros establecidos en .env para realizar la conexión a la BD
def get_connection():
    try:
        return psycopg2.connect(
            host="aws-0-us-east-2.pooler.supabase.com",
            user="writer_user.upevccqurtfvymmgrhoa",
            password="writer970",
            database="postgres",
            port=6543
        )
    except DatabaseError as ex:
        raise ex