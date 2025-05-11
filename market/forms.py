from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')

class SellItemForm(FlaskForm):
    name = StringField(label="Nombre del Ítem", validators=[DataRequired(), Length(min=2, max=30)])
    price = IntegerField(label="Precio", validators=[DataRequired()])
    description = StringField(label="Descripción", validators=[DataRequired(), Length(min=5, max=1024)])
    submit = SubmitField(label="Publicar Ítem")

class NuevaDireccionForm(FlaskForm):
    calle = StringField('Calle', validators=[DataRequired(), Length(min=2, max=100)])
    ciudad = StringField('Ciudad', validators=[DataRequired(), Length(min=2, max=50)])
    estado = StringField('Estado', validators=[DataRequired(), Length(min=2, max=50)])
    codigo_postal = StringField('Código Postal', validators=[DataRequired(), Length(min=4, max=10)])
    submit = SubmitField('Guardar')
