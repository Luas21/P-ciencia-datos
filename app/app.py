from flask import Flask, render_template, jsonify
from config import config
from routes import maquina
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

@app.route('/historico')
def historico():
    historico = 'hola'
    return render_template('historico.html',historico=historico)

def page_not_found(error):
    return "<h1>Nada por aquí...</h1>", 404

if __name__=='__main__':
    app.config.from_object(config['development'])

    app.register_blueprint(maquina.main, url_prefix='/detalle/<index>')

    app.register_error_handler(404, page_not_found)
    app.run()
