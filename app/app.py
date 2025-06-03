from flask import Flask, render_template, jsonify, request
#from config import config
from routes import maquina, historico
from models.maquinaModel import MaquinaModel

app = Flask(__name__)

@app.route('/')
def index():
    try:
        maquina=MaquinaModel.get_maquina()
        maquinas = maquina
        informacion = {
        'titulo': 'Panel de control',
        'maquinas': maquinas
        }       
        return render_template('index.html', informacion=informacion) 
    except Exception as ex:
        return jsonify({'message': str(ex)}),500

@app.route('/Historico')
def get_historico():
    try:
        historico = 'hola'
        return render_template('historico.html',historico=historico)
    except Exception as ex:
        return jsonify({'message': str(ex)}),500
    
@app.route('/api/graficos', methods=['POST'])
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

@app.route('/')
def get_maquina(id):
    try:
        info_maquina = MaquinaModel.get_info_maquina(id) 
        return render_template('detalle_maquina.html', maquina=info_maquina)
    except Exception as ex:
        return jsonify({'message': str(ex)}),500
    

def page_not_found(error):
    return "<h1>Nada por aquí...</h1>", 404

if __name__=='__main__':
    #app.config.from_object(config['development']) 

    #registro de otras rutas
    #app.register_blueprint(maquina.main, url_prefix='/detalle/<index>')
    #app.register_blueprint(historico.main, url_prefix='/Historico')

    app.register_error_handler(404, page_not_found)
    app.run()
