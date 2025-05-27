from database.db import get_connection
from .entities.Maquina import Maquina

class MaquinaModel():

    #consulta para Index, obtener la información más reciente basado en fechas.
    @classmethod
    def get_maquina(self):
        try:
            connection=get_connection()
            maquinas=[]

            with connection.cursor() as cursor:
                #cursor.execute("SELECT * FROM maquina")
                cursor.execute("""
                                 SELECT t.*
                                 FROM maquina t
                                 INNER JOIN (
                                     SELECT machine_id, MAX(date) AS max_date
                                     FROM maquina
                                     GROUP BY machine_id
                                 ) latest ON t.machine_id = latest.machine_id AND t.date = latest.max_date
                                 ORDER BY machine_id ASC
                             """)
                resulset=cursor.fetchall()

                for row in resulset:
                    maquina = Maquina(*row)
                    json_data = maquina.to_JSON()
                    json_data['estado'] = 'Normal'  # Estado estático de momento
                    maquinas.append(json_data)

            connection.close()
            return maquinas
        except Exception as es:
            raise Exception(es)
    
    #consulta para detalle_maquina, obtener la información del registro seleccionado.
    @classmethod
    def get_info_maquina(self,index):
        try:
            connection = get_connection()
            info_maquinas = []

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT t.*
                    FROM maquina t
                    WHERE t.index = %s
                """, (index,))
                resulset = cursor.fetchall()

                for row in resulset:
                    maquina = Maquina(*row)
                    json_data = maquina.to_JSON()
                    json_data['estado'] = 'Normal' #Estado estático de momento
                    info_maquinas.append(json_data)
                    
            connection.close()
            return info_maquinas[0] if info_maquinas else None

        except Exception as es:
            raise Exception(es)