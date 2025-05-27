from flask import Blueprint, jsonify, render_template
from models.maquinaModel import MaquinaModel

main=Blueprint('maquina_blueprint',__name__)

#Para mantener el app.py más limpio, se movió la ruta para poder consultar información de una máquina
@main.route('/')
def get_maquina(index):
    try:
        info_maquina = MaquinaModel.get_info_maquina(index) 
        return render_template('detalle_maquina.html', maquina=info_maquina)
    except Exception as ex:
        return jsonify({'message': str(ex)}),500
    
    