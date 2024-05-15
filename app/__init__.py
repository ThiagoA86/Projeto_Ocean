from flask import Flask

from config import Config
import sqlite3
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()



def create_app(config_class=Config):
    UPLOAD_FOLDER = 'app/temp/files'
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key ='12345'
    app.debug=True
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    csrf.init_app(app)
    # Initialize Flask extensions here

    #from app.libs.connection import Connection
    
    ########################################################
    #################  BANCO DE DADOS  #####################
    ########################################################

    # Arquivo do banco de dados
    DATABASE_PATH = 'app/config_db/db_pre_proc.db'
    sqlite3.connect(DATABASE_PATH)

    # Criando as tabelas necessárias
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS CONNECTION(
        ID INTEGER PRIMARY KEY AUTOINCREMENT, -- 0
        CONN_NAME CHAR(20) NOT NULL, -- 1
        DRIVER CHAR(20), -- 2
        HOST CHAR(20), -- 3
        PORT CHAR(4), -- 4
        CONN_DB CHAR(20), -- 5
        USERNAME CHAR(50), -- 6
        PASSWORD CHAR(20) -- 7
    )"""
    cursor.execute(query)

    query_tb_dataset = """CREATE TABLE IF NOT EXISTS DATASET(
        ID INTEGER PRIMARY KEY AUTOINCREMENT, -- 0
        CONN_ID INT NOT NULL, -- 1
        DS_NAME CHAR(50) NOT NULL, -- 2
        DS_UPD_PERIOD CHAR(20) NOT NULL, -- 3
        DS_UPD_DAY INT NOT NULL, -- 4
        DS_SCHEMA CHAR(50) NOT NULL, -- 5
        DS_TABLE CHAR(50) NOT NULL, -- 6
        DS_UPDT_TYPE INT NOT NULL default 1, -- 7
        DS_AUTO_UPDT BOOLEAN NOT NULL, -- 8
        DS_LAST_UPDT TIMESTAMP, -- 9
        DS_CREATE_METADATA BOOLEAN NOT NULL, -- 10
        FOREIGN KEY(CONN_ID) REFERENCES CONNECTION(ID)
    )"""
    cursor.execute(query_tb_dataset)
    conn.commit()
    conn.close()
    ####################################################
    ############ BLUE PRINTS ###########################
    ####################################################
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.conjunto_dados import bp as conjunto_dados_bp
    app.register_blueprint(conjunto_dados_bp,url_prefix='/conjunto_dados')

    from app.conversor import bp as conversor_bp
    app.register_blueprint(conversor_bp, url_prefix='/conversor')

    from app.conexao import bp as conexao_bp
    app.register_blueprint(conexao_bp,url_prefix='/conexao') 
    
    from app.concatenar_tabela import bp as concatenar_tabela_bp
    app.register_blueprint(concatenar_tabela_bp,url_prefix='/concatenar_tabela')

    from app.login import bp as login_bp
    app.register_blueprint(login_bp,url_prefix='/login')

    

   

    return app