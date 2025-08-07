from flask import Flask, jsonify
import datetime
import socket

# Inicializamos la aplicación Flask
app = Flask(__name__)

@app.route('/')
def home():
    """
    Endpoint principal que devuelve un mensaje de bienvenida.
    """
    return jsonify({
        "message": "¡Saludos desde el contenedor!",
        "application": "API de Status Check",
        "version": "1.0.0"
    })

@app.route('/status')
def status():
    """
    Endpoint que devuelve el estado actual y la hora del servidor.
    """
    return jsonify({
        "status": "OK",
        "server_time_utc": datetime.datetime.utcnow().isoformat()
    })

@app.route('/hostname')
def get_hostname():
    """
    Endpoint que devuelve el hostname del contenedor/máquina.
    Es útil para demostrar el aislamiento de los contenedores.
    """
    hostname = socket.gethostname()
    return jsonify({
        "hostname": hostname
    })

# Punto de entrada para ejecutar la aplicación
if __name__ == '__main__':
    # Escucha en todas las interfaces de red (0.0.0.0)
    # y en el puerto 5000
    app.run(host='0.0.0.0', port=5000)