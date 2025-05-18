import requests
from market import db
from market import app
from market.models import Direccion
from market.models import Item, User
from market.forms import NuevaDireccionForm
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm



@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        #Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')
        #Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')


        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

@app.route('/create_item', methods=['GET', 'POST'])
@login_required
def create_item_page():
    form = SellItemForm()
    if form.validate_on_submit():
        new_item = Item(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            owner=current_user.id  # Asigna el ítem al usuario autenticado
        )
        db.session.add(new_item)
        db.session.commit()
        flash(f"Item '{new_item.name}' ha sido publicado con éxito con código de barras {new_item.barcode}.", category='success')
        return redirect(url_for('market_page'))

    return render_template('create_item.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/perfile')
@login_required
def perfile_page():
    direcciones = Direccion.query.filter_by(usuario_id=current_user.id).all()
    publicaciones = Item.query.filter_by(owner=current_user.id).all()
    return render_template('perfile.html', user=current_user, direcciones=direcciones, publicaciones=publicaciones)

@app.route('/nueva_direccion', methods=['GET', 'POST'])
@login_required
def nueva_direccion():
    if request.method == 'POST':
        calle = request.form.get('calle')
        ciudad = request.form.get('ciudad')
        estado = request.form.get('estado')
        cp = request.form.get('cp')

        if calle and ciudad and estado and cp:
            nueva_dir = Direccion(
                calle=calle,
                ciudad=ciudad,
                estado=estado,
                cp=cp,
                usuario_id=current_user.id
            )
            db.session.add(nueva_dir)
            db.session.commit()
            flash("Dirección guardada correctamente", category="success")
            return redirect(url_for('perfile_page'))
        else:
            flash("Todos los campos son requeridos", category="danger")

    return render_template('nueva_direccion.html')

@app.route('/editar_direccion/<int:direccion_id>', methods=['GET', 'POST'])
@login_required
def editar_direccion(direccion_id):
    direccion = Direccion.query.get_or_404(direccion_id)
    if direccion.usuario_id != current_user.id:
        flash("No tienes permiso para editar esta dirección.", "danger")
        return redirect(url_for('perfile_page'))

    if request.method == 'POST':
        direccion.calle = request.form.get('calle')
        direccion.ciudad = request.form.get('ciudad')
        direccion.estado = request.form.get('estado')
        direccion.cp = request.form.get('cp')
        db.session.commit()
        flash('Dirección actualizada correctamente.', 'success')
        return redirect(url_for('perfile_page'))

    return render_template('editar_direccion.html', direccion=direccion)

@app.route('/eliminar_direccion/<int:direccion_id>', methods=['POST'])
@login_required
def eliminar_direccion(direccion_id):
    direccion = Direccion.query.get_or_404(direccion_id)
    if direccion.usuario_id != current_user.id:
        flash("No tienes permiso para eliminar esta dirección.", "danger")
        return redirect(url_for('perfile_page'))

    db.session.delete(direccion)
    db.session.commit()
    flash("Dirección eliminada correctamente.", "success")
    return redirect(url_for('perfile_page'))


@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
@login_required
def add_to_cart(item_id):
    item = Item.query.get_or_404(item_id)

    payload = {
        'id': item.id,
        'name': item.name,
        'price': item.price,
        'user_id': current_user.id
    }

    try:
        # Envía los datos al microservicio del carrito
        response = requests.post('http://carrito:5002/add_item', json=payload)
        if response.status_code == 200:
            flash(f'{item.name} agregado al carrito con éxito.', category='success')
        else:
            flash('Error al agregar al carrito.', category='danger')
    except Exception as e:
        flash(f'Error de conexión con el carrito: {str(e)}', category='danger')

    return redirect(url_for('market_page'))


@app.route('/api/direcciones')
def obtener_direcciones():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id requerido'}), 400

    direcciones = Direccion.query.filter_by(usuario_id=user_id).all()
    return jsonify([
        {
            'id': d.id,
            'calle': d.calle,
            'ciudad': d.ciudad,
            'estado': d.estado,
            'cp': d.cp
        }
        for d in direcciones
    ])



