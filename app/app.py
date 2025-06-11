from flask import Flask, render_template, jsonify, request
from decouple import config
from routes import historico
from models.maquinaModel import MaquinaModel

app = Flask(__name__)
app.register_blueprint(historico.main, url_prefix='/Historico')

@app.route('/')
def index():
    try:
        maquinas=MaquinaModel.get_maquina()

        informacion = {
        'titulo': 'Panel de control',
        'maquinas': maquinas
        }       
        return render_template('index.html', informacion=informacion) 
    except Exception as ex:
        return jsonify({'message': str(ex)}),500

@app.route('/detalle_maquina/<int:id>')
def get_maquina(id):
    try:
        info_maquina = MaquinaModel.get_info_maquina(id) 
        return render_template('detalle_maquina.html', maquina=info_maquina)
    except Exception as ex:
        return jsonify({'message': str(ex)}),500
    

def page_not_found(error):
    return "<h1>Nada por aquí...</h1>", 404

if __name__=='__main__':

    app.register_error_handler(404, page_not_found)
    app.run()
