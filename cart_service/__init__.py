from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'superclave-secreta-123'  # Cambia esto por algo más fuerte en producción
