from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
# Simulando almacenamiento temporal en memoria
carrito = []

@app.route('/')
def index():
    return render_template('cart.html', items=carrito)

carrito = []  # Simulación de carrito en memoria

@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.get_json()
    carrito.append(data)  # Puedes usar una base de datos real aquí
    return jsonify({'message': 'Item agregado al carrito'}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
