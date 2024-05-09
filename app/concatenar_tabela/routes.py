from app.concatenar_tabela import bp
from flask import render_template, request, send_file,jsonify
from app.libs.data import Data
import os
from werkzeug.utils import secure_filename
from app.libs.formularios import Form_Concatenar

UPLOAD_FOLDER = 'app\\temp\\files\\'
ALLOWED_EXTENSIONS = set(['csv'])
def allowed_file(filename):
     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@bp.route('/')
def index():
     formulario = Form_Concatenar()
     return render_template('concatenar_tabela.html',formulario=formulario)


# Página de funcionalidade de concatenação de tabelas do formulario /upload
@bp.route('/upload', methods=('GET','POST'))
def upload():
    formulario = Form_Concatenar()
    if request.method == 'POST' and formulario.validate():
      # recupera o arquivo enviado no request usando o post
      print(f' Validação Oi Oi Ola')
    # Salvando arquivo 1
    file_1 = formulario.arquivo1.data
    savePath_1 = os.path.join(UPLOAD_FOLDER, secure_filename(file_1.filename))

    # Salvando arquivo 2
    file_2 = formulario.arquivo2.data
    savePath_2 = os.path.join(UPLOAD_FOLDER, secure_filename(file_2.filename))

    try:
        # Concatena dois arquivos no formato csv e salva o arquivo concatenado
        Data.concatenate(file_1, file_2, UPLOAD_FOLDER)

    except Exception as e:
        msg_erro = "ERRO - NÃO FOI POSSÍVEL CONCATENAR OS ARQUIVOS: {}".format(e)
        return jsonify({'htmlresponse': render_template('response.html', msg_erro=msg_erro)})
    else:
        # Baixa o arquivo concatenado
        msg_sucesso = "Arquivo concatenado com sucesso"
        arquivo_concatenado = file_1.filename
        return jsonify({'htmlresponse': render_template('response.html', msg_sucesso=msg_sucesso, arquivo_concatenado=arquivo_concatenado)})

# Faz o download do arquivo.
@bp.route('/download/<file>')
def download_file(file):
    p = os.path.join('temp/files', file)    
    return send_file(p, as_attachment=True)