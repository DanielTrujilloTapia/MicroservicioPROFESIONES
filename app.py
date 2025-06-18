from flask import Flask, jsonify
from routes import profesiones_bp

app = Flask(__name__)

# Registrar las rutas con prefijo '/api'
app.register_blueprint(profesiones_bp, url_prefix='/api')

# Ruta raíz
@app.route('/')
def home():
    return jsonify({"message": "Microservicio Flask para profesiones funcionando"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
