from database.db import get_connection
from .entities.Maquina import Maquina
from flask import jsonify
import pandas as pd

class MaquinaModel():

    #consulta para Index, obtener la información más reciente basado en fechas.
    @classmethod
    def get_maquina(self):
        try:
            connection=get_connection()
            maquinas=[]

            with connection.cursor() as cursor:
                cursor.execute("""
                                 SELECT *
                                 FROM machine_data t
                                 INNER JOIN (
                                     SELECT machine_id, MAX(date) AS max_date
                                     FROM machine_data
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
    def get_info_maquina(self,id):
        try:
            connection = get_connection()
            info_maquinas = []

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT t.*
                    FROM machine_data t
                    WHERE t.id = %s
                """, (id,))
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


    @classmethod
    def get_historico_maquina(self, start_date, end_date):
        try:
            connection = get_connection()

            query = """
                SELECT date, machine_id, downtime
                FROM machine_data
                WHERE date BETWEEN %s AND %s
                ORDER BY date ASC
            """

            with connection.cursor() as cursor:
                cursor.execute(query, (start_date, end_date))
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

            connection.close()

            df = pd.DataFrame(rows, columns=columns)
            
            # Convertir a datetime y extraer año-mes
            df['date'] = pd.to_datetime(df['date'])
            df['month_str'] = df['date'].dt.to_period('M').astype(str)  # '2025-04', '2025-05', etc.

            fecha_min = df['date'].min().strftime('%Y-%m-%d')
            fecha_max = df['date'].max().strftime('%Y-%m-%d')

            df['downtime'] = df['downtime'].astype(int)

            funcionando = len(df[df['downtime'] == 0])
            caido = len(df[df['downtime'] == 1])

            meses = sorted(df['month_str'].unique())

            grouped = df.groupby(['month_str', 'machine_id', 'downtime']).size().reset_index(name='count')
            grouped['machine_id_str'] = grouped['machine_id'].astype(str)

            maquinas = {}
            for machine_id in df['machine_id'].unique():
                estados = []
                for mes in meses:
                    match = grouped[
                        (grouped['month_str'] == mes) &
                        (grouped['machine_id_str'] == str(machine_id)) &
                        (grouped['downtime'] == 1)
                    ]
                    count = match['count'].sum() if not match.empty else 0
                    estados.append(int(count))
                maquinas[machine_id] = estados

            return {
                'funcionando': funcionando,
                'caido': caido,
                'fechas': meses,
                'maquinas': maquinas,
                'fecha_min': fecha_min,
                'fecha_max': fecha_max
            }

        except Exception as e:
            return {'error': str(e)}
