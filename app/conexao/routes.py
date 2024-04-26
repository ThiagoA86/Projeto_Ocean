from  app.conexao import bp
from flask import render_template, request, redirect, url_for,flash
from app.libs.connection import Connection


@bp.route('/')
def index():
    
     #Lista as conexões cadastrada e redenriza a View       
     data = Connection.list_all_conn()
     return render_template("conexao.html", data=data)
            
@bp.route('/insert',methods=('GET','POST'))  
def insert():
     # Salvando a conexão, passado pelo formulario da Conexao.html
     if request.method == "POST":
        database = request.form['database']
        if database == '':
            flash("O nome do database não pode ser vazio", 'error')
            return redirect(url_for('conexao.index'))
        #elif Connection.get_single_conn(id):
        #    flash("A conexão '{}' já existe!".format(database), 'error')
        #    return redirect(url_for('conexao'))
        else:
            try:
                driver = request.form['driver']
                nomeconexao = request.form['nome_conexao']
                host = request.form['host']
                porta = request.form['porta']
                database = request.form['database']
                username = request.form['username']
                password = request.form['password']
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
    if request.method == 'POST':
        new_database = request.form['database']
        #Esse condicional provavelmente não precisa, pois o formulario do Front-End restringe.
        if new_database == '':
            flash("O nome da conexão não pode ficar vazio!", 'error')
            return(redirect(url_for('conexao')))
        else:
            try:
                driver = request.form['driver']
                host = request.form['host']
                porta = request.form['porta']
                new_database = request.form['database']
                username = request.form['username']
                password = request.form['password']

                nome_conexao = request.form['nome_conexao']
                #Recebe as varaives de cima e passa para o metodo update_conn da Libs Conection
                Connection.update_conn(driver, nome_conexao, host, porta, new_database, username, password, id)
            except Exception as e:
                flash('Não foi possível atualizar a conexão: {}'.format(e), 'error')
                return redirect(url_for('conexao.index'))
            else:
                flash('Atualização feita com sucesso!', 'success')
                return redirect(url_for('conexao.index'))
            
@bp.route('/delete/<string:id>',methods=('GET','POST'))
def delete(id):
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