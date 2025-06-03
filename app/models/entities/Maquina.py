from utils.DateFormat import DateFormat

class  Maquina:
    #Establecemos el formato general para obtener toda la información de nuestra tabla.
    def __init__(self, id=None, date=None, machine_id=None, assembly_line_no=None, hydraulic_pressure_bar=None, coolant_pressure_bar=None, air_system_pressure_bar=None, coolant_temperature=None, hydraulic_oil_temperature=None, spindle_bearing_temperature=None, spindle_vibration=None, tool_vibration=None, spindle_speed_rpm=None, voltage_volts=None, torque_nm=None, cutting_kn=None, downtime=None):
        self.id = id
        self.date = date
        self.machine_id = machine_id
        self.assembly_line_no = assembly_line_no
        self.hydraulic_pressure_bar = hydraulic_pressure_bar
        self.coolant_pressure_bar = coolant_pressure_bar
        self.air_system_pressure_bar = air_system_pressure_bar
        self.coolant_temperature = coolant_temperature
        self.hydraulic_oil_temperature = hydraulic_oil_temperature
        self.spindle_bearing_temperature = spindle_bearing_temperature
        self.spindle_vibration = spindle_vibration
        self.tool_vibration = tool_vibration
        self.spindle_speed_rpm = spindle_speed_rpm
        self.voltage_volts = voltage_volts
        self.torque_nm = torque_nm
        self.cutting_kn = cutting_kn
        self.downtime = downtime

    #función para poder obtener todo en formato JSON
    def to_JSON(self):
        return {
            'id': self.id,
            'date': self.date,
            'machine_id': self.machine_id,
            'assembly_line_no': self.assembly_line_no,
            'hydraulic_pressure_bar': self.hydraulic_pressure_bar,
            'coolant_pressure_bar': self.coolant_pressure_bar,
            'air_system_pressure_bar': self.air_system_pressure_bar,
            'coolant_temperature': self.coolant_temperature,
            'hydraulic_oil_temperature': self.hydraulic_oil_temperature,
            'spindle_bearing_temperature': self.spindle_bearing_temperature,
            'spindle_vibration': self.spindle_vibration,
            'tool_vibration': self.tool_vibration,
            'spindle_speed_rpm': self.spindle_speed_rpm,
            'voltage_volts': self.voltage_volts,
            'torque_nm': self.torque_nm,
            'cutting_kn': self.cutting_kn,
            'downtime': self.downtime
        }
