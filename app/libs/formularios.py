from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField,SelectField, FileField  
from wtforms.validators import DataRequired, InputRequired, Length
from flask_wtf.file import FileAllowed, FileRequired
from werkzeug.security import generate_password_hash 



########################################################
#################  CLASS FORMULARIOS  ##################
########################################################

class Form_Conexao(FlaskForm):

    #Atributos da CONEXAO#
    nome_conexao = StringField('Nome da Conexão:', validators=[InputRequired()])
    host = StringField('Host:',validators=[DataRequired(), Length(min=7, max=16)])
    porta = StringField('Porta:',validators=[DataRequired(), Length(min=4, max=4)])
    database = StringField('Database:', validators=[InputRequired()])
    username = StringField('Username:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()]) 
    driver = SelectField('Driver:', choices=[('oracle', 'Oracle'), ('postgresql', 'PostgreSQL')]) 

class Form_Conjunto_de_dados(FlaskForm):
    #Atributos da CONJUNTO DE DADOS#
    titulo = StringField('Título:', validators=[InputRequired()])
    freq_atualizacao = SelectField('Frequência de atualização:', choices=[('diario', 'Diario'),('semanal', 'Semanal'), 
                                                      ('mensal', 'Mensal'),
                                                      ('semestral', 'Semestral'),('anual', 'Anual')])
    dia_atualizacao=SelectField('Dia:', choices=[(str(i), str(i)) for i in range(1, 32)])
    schema = StringField('Schema:', validators=[InputRequired()])
    tabela = StringField('Tabela:', validators=[InputRequired()])
    tipo_atualizacao = SelectField('Tipo de atualização:', choices=[('simples', 'Simples'), ('com concatenação', 'Com concatenação')]) 
    atualizacao_automatica = BooleanField('Atualização automática.')
    criar_metadados =BooleanField('Criar os metadados ao adicionar.')
    ultima_atu= StringField('Última atualização:')
class Form_Conversor(FlaskForm):     
     #Atributos do CONVERSOR#
    arquivo = FileField('Selecione um arquivo PDF:',validators=[FileRequired(),FileAllowed(['pdf'],'Apenas arquivos PDF são permitidos.')])
    
class Form_Concatenar(FlaskForm):     
     #Atributos do CONTENARR#
    arquivo1 = FileField('Arquivo 1:',validators=[FileRequired(),FileAllowed(['csv'],'Apenas arquivos CSV são permitidos.')])
    arquivo2 = FileField('Arquivo 2:',validators=[FileRequired(),FileAllowed(['csv'],'Apenas arquivos CSV são permitidos.')])
    #Atributos do LOGIN#