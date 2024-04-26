from app.conjunto_dados import bp
from flask import render_template, request, redirect, url_for, flash
from app.libs.connection import Connection
from app.libs.dataset import Dataset
from datetime import date

# Página de conjuntos de dados
@bp.route('/')
def index():
     #Lista as conexões cadastrada do Lib Dataset.py
     data = Dataset.list_all_dataset()
     #Lista as conexões cadastrada do Lib Connection.py
     data_conn = Connection.list_all_conn()
     return render_template("conjunto_dados.html", data=data, data_conn=data_conn)

   

# Funcionalidade de salvar informações do conjunto de dados, passado pelo formulario da Conjunto_dados.html
@bp.route('/ds_insert',methods=('GET','POST'))
def ds_insert():
    if request.method == 'POST':
        try:
            conn_id = request.form['database']
            titulo = request.form['titulo']
            freq_atualizacao = request.form['freq_atualizacao']
            dia = request.form['dia_atualizacao']
            schema = request.form['schema']
            table = request.form['table']
            tipo_atualizacao = request.form['tipo_atualizacao']
            atualizacao_automatica = True if request.form.get('atualizacao_automatica') else False
            criar_metadados = True if request.form.get('metadata') else False
            ultima_atualizacao = 0
            #print(tipo_atualizacao) # Teste para ver ser o tipo de atualização escolhido aparece
            # Usa metodo add_dataset da Libs Dataset.py
            Dataset.add_dataset(conn_id, titulo, freq_atualizacao, dia, schema, table, tipo_atualizacao, ultima_atualizacao, atualizacao_automatica, criar_metadados)
        except Exception as e:
            flash("Não foi possível criar o conjunto de dados : {}".format(e), 'error')
            return redirect(url_for('conjunto_dados.index'))  
        else:
            flash("Conjunto de dados criado com sucesso!", 'success')
            return redirect(url_for('conjunto_dados.index'))

# Funcionalidade de editar informações do conjunto de dados já salvo, passado pelo formulario da Conjunto_dados.html
@bp.route('/ds_edit/<string:id>',methods=('GET','POST'))
def ds_edit(id):
    if request.method == 'POST':
        new_titulo = request.form['titulo']
        if new_titulo == '':
            flash("O nome do conjunto de dados não pode ficar vazio!", 'error')
            return(redirect(url_for('conjunto_dados.index')))
        else:
            try:
                conn_id = request.form['database']
                titulo = request.form['titulo']
                freq_atualizacao = request.form['freq_atualizacao']
                dia = request.form['dia_atualizacao']
                schema = request.form['schema']
                database = request.form['database']
                table = request.form['table']
                tipo_atualizacao = request.form['tipo_atualizacao']
                ultima_atualizacao = str(date.today())
                atualizacao_automatica = True if request.form.get('atualizacao_automatica') else False
                criar_metadados = True if request.form.get('metadata') else False
                #Recebe ID e passa para o metodo edit_dataset da Libs Dataset.py
                Dataset.edit_dataset(id, conn_id, titulo, freq_atualizacao, dia, schema, database, table, tipo_atualizacao, ultima_atualizacao, atualizacao_automatica, criar_metadados)
            except Exception as e:
                flash('Não foi possível salvar as informações atualizadas do conjunto de dados: {}'.format(e), 'error')
                return redirect(url_for('conjunto_dados.index'))
            else:
                flash('Informações do conjunto de dados atualizada com sucesso!', 'success')
                return redirect(url_for('conjunto_dados.index'))

# Funcionalidade de atualizar o conjunto de dados e catalogá-lo ao portal CKAN, passado pelo formulario da Conjunto_dados.html 
@bp.route('/ds_update/<string:id>', methods=('GET','POST'))
def ds_update(id):
    if request.method == 'POST':
        try:
            dataset = Dataset.get_single_dataset(id)
            print(dataset)
            print(dataset[0][1])
            Dataset.update_dataset(dataset) 
        except Exception as e:
            flash('Não foi possível atualizar o conjunto de dados "{}" : {}'.format(dataset[0][2],e), 'error')
            return redirect(url_for('conjunto_dados.index'))
        else:
            flash('Conjunto de dados atualizado com sucesso', 'success')
            return redirect(url_for('conjunto_dados.index'))
        

# Funcionalidade de remover conjunto de dados, passado pelo formulario da Conjunto_dados.html
@bp.route('/ds_delete/<string:id>', methods=('GET','POST'))
def ds_delete(id):
    if request.method == 'POST':
        try:
            #Recebe ID e passa para o metodo delete_dataset da Libs Dataset.py
            Dataset.delete_dataset(id)
        except Exception as e:
            flash("Não foi possível remover o conjunto de dados: {}".format(e), 'error')
            return redirect(url_for('conjunto_dados.index'))
        else:
            flash('Conjunto de dados removido com sucesso!', 'success')
            return redirect(url_for('conjunto_dados.index'))
