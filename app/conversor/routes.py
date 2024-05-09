from  app.conversor import bp
from flask import render_template, request, send_file
import platform
import subprocess
import os
import shutil
from app.libs.formularios import Form_Conversor

@bp.route('/')
def index():
     formulario=Form_Conversor()
     if not os.path.exists('app/files'):
        os.makedirs('app/files/pdf')
        os.makedirs('app/files/txt')
         
     else:
        #pass    
          try:
            os.makedirs('app/files/pdf')
            os.makedirs('app/files/txt') 
          except FileExistsError:
            pass
       
            
     return render_template('conversor.html',formulario=formulario)



@bp.route('/converter_file', methods=('POST','GET'))
def converter_file():
    # Salva o sistema operacional em que o aplicativo está sendo executado
    sist_op = platform.system()
    formulario=Form_Conversor()
    # Atribuindo o caminho do pdf e do conversor conforme o sistema operacional detectado ( Windows ou Linux )
    pdf_path = "app\\files\\pdf\\" if sist_op == 'Windows' else "app//files//pdf//"
    txt_path = "app\\files\\txt\\" if sist_op == 'Windows' else "app//files//txt//"
    bin_path = "app\\bin\\windows\\" if sist_op == "Windows" else "app//bin//linux//"
    if request.method == "POST" and formulario.validate():
            # recupera o arquivo enviado no request usando o post
      print(f' Validação Oi Oi Ola')
    arquivo = formulario.arquivo.data
    #arquivo = request.files['arquivo']
    #salva o nome do arquivo na variável filename
    filename = formulario.arquivo.data.filename

    # Salva o arquivo no sistema de arquivos
    arquivo.save(filename)

    # Move o arquivo para o diretório adequado
    shutil.move(filename, pdf_path)

    # Cria o caminho do arquivo de texto
    dir_arq_conv = os.path.join(txt_path, filename.replace(".pdf", ".txt"))

    # Executar o comando pdftotext para converter o texto, o resultado da execução é capturado com capture_output=True
    # Verifica se a conversão foi bem-sucedida, verificando o código de retorno do comando pdftotext usando .returncode.
    # Se for igual a 0, significa que a conversão foi concluída com sucesso
 
    if subprocess.run([bin_path+'pdftotext','-layout', pdf_path + filename, dir_arq_conv], capture_output=True).returncode == 0:
        # Remover o arquivo PDF após a conversão 
        os.remove(pdf_path + filename)
        filename = filename.replace(".pdf", ".txt")
        
        return render_template('resposta-conversor.html',arquivo_convertido=filename)
    else:
        return 'A conversão falhou'

@bp.route('/download_txt/<file>')
def download_txt(file):
    p = os.path.join('files/txt/', file)
    return send_file(p, as_attachment=True)
