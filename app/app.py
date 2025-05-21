from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    maquinas = ['maquina 1','maquina 2']
    informacion = {
        'titulo': 'Panel de control',
        'maquinas': maquinas
    }
    return render_template('index.html', informacion=informacion)

@app.route('/historico')
def historico():
    historico = 'hola'
    return render_template('historico.html',historico=historico)

if __name__=='__main__':
    app.run(debug=True)
