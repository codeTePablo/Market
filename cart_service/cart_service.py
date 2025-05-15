from flask import Flask, request, jsonify, render_template, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'superclave-secreta-123'  # Cambia esto por algo más fuerte en producción
# Simulando almacenamiento temporal en memoria
carrito = {}  # Ahora es un diccionario por usuario

@app.route('/')
def show_cart():
    user_id = request.args.get('user_id')
    if not user_id:
        return "user_id requerido", 400
    items = carrito.get(user_id, [])
    total = sum(item['price'] for item in items)
    return render_template('cart.html', items=items, total=total, user_id=user_id)

@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.json
    item = {
        "id": data.get("id"),
        "name": data.get("name"),
        "price": data.get("price")
    }
    user_id = str(data.get("user_id"))
    if user_id:
        carrito.setdefault(user_id, []).append(item)
        return jsonify({"message": "Item agregado", "item": item})
    return jsonify({"error": "user_id requerido"}), 400

@app.route('/remove_item', methods=['POST'])
def remove_item():
    item_id = request.form.get('item_id')
    user_id = request.form.get('user_id')
    if user_id and item_id:
        carrito[user_id] = [item for item in carrito.get(user_id, []) if str(item.get('id')) != str(item_id)]
        flash('Artículo eliminado del carrito.', 'success')
        return redirect(url_for('show_cart', user_id=user_id))
    flash('Datos inválidos.', 'danger')
    return redirect('/')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
