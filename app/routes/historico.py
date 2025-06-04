from flask import Blueprint, jsonify, render_template, request
from models.maquinaModel import MaquinaModel

main=Blueprint('historico',__name__)

@main.route('/')
def get_historico():
    try:
        historico = 'hola'
        return render_template('historico.html',historico=historico)
    except Exception as ex:
        return jsonify({'message': str(ex)}),500
    
@main.route('/api/graficos', methods=['POST'])
def api_graficos():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON no recibido o inválido'}), 400

        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if not start_date or not end_date:
            return jsonify({'error': 'Faltan fechas en el JSON'}), 400

        resultado = MaquinaModel.get_historico_maquina(start_date, end_date)
        return resultado  

    except Exception as ex:
        return jsonify({'error': str(ex)}), 500