import requests
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

@app.route('/confirmacion')
def confirmar_compra():
    user_id = request.args.get('user_id')
    if not user_id:
        return "user_id requerido", 400

    # Hacemos un GET al microservicio 'market' para obtener las direcciones
    try:
        res = requests.get(f'http://market:5000/api/direcciones?user_id={user_id}')
        if res.status_code != 200:
            return f"Error al obtener direcciones: {res.text}", res.status_code
        direcciones = res.json()
    except Exception as e:
        return f"Error al conectar con market: {str(e)}", 500

    return render_template('confirmacion.html', direcciones=direcciones, user_id=user_id)

@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    # Recuperas user_id y direccion_id del form
    user_id = request.form.get('user_id')
    direccion_id = request.form.get('direccion_id')
    if not user_id or not direccion_id:
        return "Faltan datos de usuario o dirección", 400

    # Vuelve a cargar los ítems del carrito
    items = carrito.get(user_id, [])
    total = sum(item['price'] for item in items)

    # Renderiza el template que ya creamos
    return render_template(
        'finalizar_compra.html',
        items=items,
        total=total,
        user_id=user_id,
        direccion_id=direccion_id
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
