from database.db import get_connection
from .entities.Maquina import Maquina
from flask import jsonify
import pandas as pd

class MaquinaModel():

    #consulta para Index, obtener la información más reciente basado en fechas.
    @classmethod
    def get_maquina(cls):
        try:
            connection = get_connection()
            maquinas = []

            # Obtener rangos automáticamente para poder obtener un índice_salud que nos permita conocer el estado de la máquina
            rangos = cls.obtener_rangos_sensores()
            #Los pesos obtenidos son gracias al análisis realizado en google Colab (según la importancia de cada columna para el resultado)
            pesos = {
                'hydraulic_pressure_bar': 0.43,
                'torque_nm': 0.22,
                'cutting_kn': 0.16,
                'coolant_pressure_bar': 0.09,
                'spindle_speed_rpm': 0.06
            }

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT t.id, t.date, t.machine_id, t.assembly_line_no, 
                        t.hydraulic_pressure_bar, t.coolant_pressure_bar, t.air_system_pressure_bar,
                        t.coolant_temperature, t.hydraulic_oil_temperature, t.spindle_bearing_temperature,
                        t.spindle_vibration, t.tool_vibration, t.spindle_speed_rpm, t.voltage_volts,
                        t.torque_nm, t.cutting_kn, t.downtime
                    FROM machine_data t
                    JOIN (
                        SELECT machine_id, MAX(id) as max_id
                        FROM machine_data
                        WHERE (machine_id, date) IN (
                            SELECT machine_id, MAX(date)
                            FROM machine_data
                            GROUP BY machine_id
                        )
                        GROUP BY machine_id
                    ) latest ON t.id = latest.max_id
                    ORDER BY t.machine_id;
                """)
                resulset = cursor.fetchall()

                for row in resulset:
                    maquina = Maquina(*row)
                    json_data = maquina.to_JSON()

                    # Calcular índice de salud
                    indice = 0
                    for sensor, peso in pesos.items():
                        valor = float(json_data[sensor]) if json_data[sensor] is not None else None
                        minimo = float(rangos[sensor][0])
                        maximo = float(rangos[sensor][1])
                        if valor is not None and maximo != minimo:
                            normalizado = (valor - minimo) / (maximo - minimo)
                            indice += normalizado * peso

                    json_data['indice_salud'] = round(indice, 3)

                    # Clasificar estado basado
                    if indice > 0.75:
                        json_data['estado'] = 'Crítico'
                    elif indice > 0.5:
                        json_data['estado'] = 'Necesario'
                    elif indice > 0.25:
                        json_data['estado'] = 'Recomendado'
                    else:
                        json_data['estado'] = 'Normal'

                    maquinas.append(json_data)

            connection.close()
            return maquinas

        except Exception as e:
            raise Exception(f'Error en get_maquina: {str(e)}')

    
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
            df['day_str'] = df['date'].dt.strftime('%Y-%m-%d')  # '2025-06-01', '2025-06-02', etc.

            fecha_min = df['date'].min().strftime('%Y-%m-%d')
            fecha_max = df['date'].max().strftime('%Y-%m-%d')

            df['downtime'] = df['downtime'].astype(int)

            funcionando = len(df[df['downtime'] == 0])
            caido = len(df[df['downtime'] == 1])

            # Días únicos ordenados
            dias = sorted(df['day_str'].unique())

            # Agrupar por día, máquina y estado
            grouped = df.groupby(['day_str', 'machine_id', 'downtime']).size().reset_index(name='count')
            grouped['machine_id_str'] = grouped['machine_id'].astype(str)

            maquinas = {}
            for machine_id in df['machine_id'].unique():
                estados = []
                for dia in dias:
                    match = grouped[
                        (grouped['day_str'] == dia) &
                        (grouped['machine_id_str'] == str(machine_id)) &
                        (grouped['downtime'] == 1)
                    ]
                    count = match['count'].sum() if not match.empty else 0
                    estados.append(int(count))
                maquinas[machine_id] = estados

            return {
                'funcionando': funcionando,
                'caido': caido,
                'fechas': dias,
                'maquinas': maquinas,
                'fecha_min': fecha_min,
                'fecha_max': fecha_max
            }


        except Exception as e:
            return {'error': str(e)}

    @classmethod
    def obtener_rangos_sensores(cls):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        MIN(hydraulic_pressure_bar), MAX(hydraulic_pressure_bar),
                        MIN(torque_nm), MAX(torque_nm),
                        MIN(cutting_kn), MAX(cutting_kn),
                        MIN(coolant_pressure_bar), MAX(coolant_pressure_bar),
                        MIN(spindle_speed_rpm), MAX(spindle_speed_rpm)
                    FROM machine_data;
                """)
                row = cursor.fetchone()

                rangos = {
                    'hydraulic_pressure_bar': (row[0], row[1]),
                    'torque_nm': (row[2], row[3]),
                    'cutting_kn': (row[4], row[5]),
                    'coolant_pressure_bar': (row[6], row[7]),
                    'spindle_speed_rpm': (row[8], row[9])
                }

            connection.close()
            return rangos

        except Exception as e:
            raise Exception(f'Error al obtener rangos: {str(e)}')