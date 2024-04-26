# Essa classe é responsável pelas funcionalidades CRUD ( Create, Read, Update, Delete )
# das conexões ao banco de dados
import json
from app.libs import data # arquivo data.py

# para conexão e leitura do banco de dados
from sqlalchemy import create_engine, text

# para a leitura e exportação do banco de dados para formato csv
import pandas as pd

# Para uso do banco de dados SQLite
import sqlite3

FILEPATH = 'config/conn.json'
DATABASE_PATH = 'app/config_db/db_pre_proc.db'

class Connection:

    # Construtor da classe
    def __init__(self, Driver, NomeConexao, Host, Porta, Database, Username, Password):
        self.__Driver = Driver,
        self.__NomeConexao = NomeConexao,
        self.__Host =  Host,
        self.__Porta = Porta,
        self.__Database = Database,
        self.__Username = Username,
        self.__Password = Password

    # Adicionando conexão
    def add_conn(Driver, NomeConexao, Host, Porta, Database, Username, Password):
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        query_insert_tb_connection = ('INSERT INTO CONNECTION ( CONN_NAME, DRIVER, HOST, PORT, CONN_DB, USERNAME, PASSWORD)'
            ' VALUES ( :CONN_NAME, :DRIVER, :HOST, :PORT, :CONN_DB, :USERNAME, :PASSWORD);')

        params = {
            'CONN_NAME': NomeConexao,
            'DRIVER': Driver,
            'HOST': Host,
            'PORT': Porta,
            'CONN_DB': Database,
            'USERNAME': Username,
            'PASSWORD': Password
        }

        conn.execute(query_insert_tb_connection, params)
        conn.commit()
        conn.close()

    # Lendo dados de uma única conexão
    def get_single_conn(id):
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.execute("select * from connection where id = {}".format(id))
            return cursor.fetchall()

    # Atualizando conexão
    def update_conn(Driver, Conn_name, Host, Porta, Database, Username, Password, id):
        conn = sqlite3.connect(DATABASE_PATH)
        query_updt_connection = ('UPDATE CONNECTION SET CONN_NAME = :CONN_NAME, '
                                 'DRIVER = :DRIVER, '
                                 'HOST = :HOST, '
                                 'PORT = :PORT, '
                                 'CONN_DB = :CONN_DB, '
                                 'USERNAME = :USERNAME, '
                                 'PASSWORD = :PASSWORD '
                                 'WHERE ID = {}'.format(id))
        
        params = {
            'CONN_NAME': Conn_name,
            'DRIVER': Driver,
            'HOST': Host,
            'PORT': Porta,
            'CONN_DB': Database,
            'USERNAME': Username,
            'PASSWORD': Password
        }

        conn.execute(query_updt_connection, params)
        conn.commit()
        conn.close()

    # Deletando conexão
    def delete_conn(id):
        conn = sqlite3.connect(DATABASE_PATH)
        query_del = ("delete from connection where id = {}".format(id))
        conn.execute(query_del)
        conn.commit()
        conn.close()

    # Listando todas as conexões
    def list_all_conn():    
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.execute("select * from connection")
            return cursor.fetchall()




        