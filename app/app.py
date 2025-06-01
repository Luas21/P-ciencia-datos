from flask import Flask, render_template, jsonify
from config import config
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


def page_not_found(error):
    return "<h1>Nada por aquí...</h1>", 404

if __name__=='__main__':
    app.config.from_object(config['development'])

    #registro de otras rutas
    app.register_blueprint(maquina.main, url_prefix='/detalle/<index>')
    app.register_blueprint(historico.main, url_prefix='/Historico')

    app.register_error_handler(404, page_not_found)
    app.run()
