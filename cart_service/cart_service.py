from flask import Flask, request, jsonify, render_template, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'superclave-secreta-123'  # Cambia esto por algo más fuerte en producción
# Simulando almacenamiento temporal en memoria
carrito = []

@app.route('/')
def index():
    return render_template('cart.html', items=carrito)

carrito = []  # Simulación de carrito en memoria

@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.json
    item = {
            "id": data.get("id"),
            "name": data.get("name"),
            "price": data.get("price")
        }
    carrito.append(item)
    return jsonify({"message": "Item agregado", "item": item})


# cart_items = []  # tu lista global o estructura usada

@app.route('/remove_item', methods=['POST'])
def remove_item():
    item_id = request.form.get('item_id')
    if item_id:
        global carrito
        carrito = [item for item in carrito if str(item.get('id')) != str(item_id)]
        flash('Artículo eliminado del carrito.', 'success')
    else:
        flash('ID no válido.', 'danger')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
