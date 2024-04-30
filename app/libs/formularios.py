from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField 
from wtforms import DecimalField, RadioField, SelectField, TextAreaField, FileField 
from wtforms.validators import DataRequired, InputRequired, Length
from werkzeug.security import generate_password_hash 



########################################################
#################  CLASS FORMULARIO  ###################
########################################################

class Form_Flask(FlaskForm):

    #Atributos da CONEXAO#
    nome_conexao = StringField('Nome da Conexão', validators=[InputRequired()])
    host = StringField('Host',validators=[DataRequired(), Length(min=7, max=16)])
    porta = StringField('Host',validators=[DataRequired(), Length(min=4, max=4)])
    database = StringField('Database', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()]) 
    driver = SelectField('Driver', choices=[('oracle', 'Oracle'), ('postgresql', 'PostgreSQL')]) 

    #Atributos da CONJUNTO DE DADOS#

    #Atributos do LOGIN#