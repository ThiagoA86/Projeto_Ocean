from  app.conexao import bp
from flask import render_template, request, redirect, url_for,flash
from app.libs.connection import Connection
from app.libs.formularios import Form_Flask
from werkzeug.security import generate_password_hash 




#Instânciando a Classe Formulario para usar nas funções.
#formulario = Form_conexao()    

@bp.route('/',methods=('GET','POST'))
def index():
    #Instânciando a Classe Formulario para usar na função. 
    formulario = Form_Flask()    
     #Lista as conexões cadastrada e redenriza a View e Class Formulario      
    data = Connection.list_all_conn()
    return render_template("conexao.html", data=data, formulario=formulario)
            
@bp.route('/insert',methods=('GET','POST'))  
def insert():
     #Instânciando a Classe Formulario para usar nas funções.
     formulario = Form_Flask()
     # Salvando a conexão, passado pelo formulario da Conexao.html
     if request.method == "POST" and formulario.validate():
        database = formulario.porta.data
        if database == '':
            flash("O nome do database não pode ser vazio", 'error')
            return redirect(url_for('conexao.index'))
        #elif Connection.get_single_conn(id):
        #    flash("A conexão '{}' já existe!".format(database), 'error')
        #    return redirect(url_for('conexao'))
        else:
            try:
                driver = formulario.driver.data
                nomeconexao = formulario.nome_conexao.data
                host = formulario.host.data
                porta = formulario.porta.data
                database = formulario.porta.data
                username = formulario.username.data
                password = formulario.password.data
                #Recebe as varaives de cima e passa para o metodo Add_conn da Libs Conection
                Connection.add_conn(driver, nomeconexao, host, porta, database, username, password)
            except Exception as e:
                flash('Não foi possível criar a conexão: {}'.format(e), 'error')
                return redirect(url_for('conexao.index'))
            finally:
                flash("Conexão criada com sucesso!", 'success')
                return redirect(url_for('conexao.index'))
               
@bp.route('/update/<string:id>',methods=('GET','POST'))
def update(id):
    #Instânciando a Classe Formulario para usar nas funções.
    formulario = Form_Flask()
    if request.method == 'POST' and formulario.validate():
        new_database = request.form['database']
        #Esse condicional provavelmente não precisa, pois o formulario do Front-End restringe.
        if new_database == '':
            flash("O nome da conexão não pode ficar vazio!", 'error')
            return(redirect(url_for('conexao')))
        else:
            try:
                driver = formulario.driver.data
                nomeconexao = formulario.nome_conexao.data
                host = formulario.host.data
                porta = formulario.porta.data
                database = formulario.porta.data
                username = formulario.username.data
                password = formulario.password.data
                #Recebe as varaives de cima e passa para o metodo update_conn da Libs Conection
                Connection.update_conn(driver, nomeconexao, host, porta, database, username, password, id)
            except Exception as e:
                flash('Não foi possível atualizar a conexão: {}'.format(e), 'error')
                return redirect(url_for('conexao.index'))
            else:
                flash('Atualização feita com sucesso!', 'success')
                return redirect(url_for('conexao.index'))
            
@bp.route('/delete/<string:id>',methods=('GET','POST'))
def delete(id):
    #Instânciando a Classe Formulario para usar nas funções.
    
    if request.method == 'POST':
        try:
            #Recebe ID e passa para o metodo delete_conn da Libs Conection
            Connection.delete_conn(id)
        except Exception as e:
            flash('Não foi possível remover a conexão: {}'.format(e), 'error')
            return redirect(url_for('conexao.index'))
        else:
            flash('Conexão removida com sucesso!','success')
            return redirect(url_for('conexao.index'))    