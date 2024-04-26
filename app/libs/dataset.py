# Essa classe é responsável pelas funcionalidades CRUD ( Create, Read, Update, Delete )
# das conexões ao banco de dados
import json
from app.libs.data import Data

# Conexão 
from app.libs.connection import Connection

# para conexão e leitura do banco de dados
from sqlalchemy import create_engine, text

# para a leitura e exportação do banco de dados para formato csv
import pandas as pd

# Para fazer a descrição do conjunto de dados
from frictionless import describe, extract, validate, Detector, Resource, Package, Pipeline, steps
from frictionless.portals import CkanControl

# Para ações de remoção de arquivos
import os

# Para extração do ano
import datetime

# Para remover acentos
import unidecode

# Para enviar os conjuntos de dados e metadados ao CKAN
import requests

# Para uso do banco de dados SQLite
import sqlite3

# Para download do arquivo csv do portal CKAN
import wget

#FILEPATH = 'config/dataset.json'
METADATAPATH = 'metadata'
url = "https://dados-staging.ufpe.br"
DATABASE_PATH = 'app/config_db/db_pre_proc.db'
#CKAN_URL = 'https://dados.ufpe.br/dataset/funcoes-gratificadas'
CKAN_URL = 'https://dados.ufpe.br/dataset'

class Dataset:

    # Construtor da classe
    def __init__(self, conn_id, titulo, freq_atualizacao, dia, schema, database, table, tipo_atualizacao, ultima_atualizacao, atualizacao_automatica):
        self.__conn_id = conn_id,
        self.__titulo = titulo,
        self.__freq_atualizacao =  freq_atualizacao,
        self.__dia = dia,
        self.__schema = schema
        self.__database = database,
        self.__table = table,
        self.__tipo_atualizacao = tipo_atualizacao,
        self.__ultima_atualizacao = ultima_atualizacao,
        self.__atualizacao_automatica = atualizacao_automatica,

    # obtem informação de um único conjunto de dados
    def get_single_dataset(id):
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.execute("select * from dataset where id = {}".format(id))
            return cursor.fetchall()

    # Lista todos os conjuntos de dados
    def list_all_dataset():
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.execute("select * from dataset")
            return cursor.fetchall()
    
    # Cadastra conjunto de dados
    def add_dataset(conn_id, titulo, freq_atualizacao, dia, schema, table, tipo_atualizacao, ultima_atualizacao, atualizacao_automatica, criar_metadados):
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        query_insert_tb_dataset = """insert into dataset(
            conn_id,
            ds_name,
            ds_upd_period,
            ds_upd_day,  
            ds_schema,
            ds_table,
            ds_updt_type,
            ds_auto_updt,
            ds_last_updt,
            ds_create_metadata)
            values(
            :conn_id,
            :ds_name,
            :ds_upd_period,
            :ds_upd_day,
            :ds_schema,
            :ds_table,
            :ds_updt_type,
            :ds_auto_updt,
            :ds_last_updt,
            :ds_create_metadata
            )
        """

        params = {
            'conn_id': conn_id,
            'ds_name': titulo,
            'ds_upd_period': freq_atualizacao,
            'ds_upd_day': dia,
            'ds_schema': schema,
            'ds_table': table,
            'ds_updt_type': tipo_atualizacao,
            'ds_auto_updt': atualizacao_automatica,
            'ds_last_updt': ultima_atualizacao,
            'ds_create_metadata': criar_metadados
        }
        cursor.execute(query_insert_tb_dataset, params)
        conn.commit()
        conn.close()

        if criar_metadados:
            database_credentials = Connection.get_single_conn(conn_id)
            Dataset.create_metadata_ckan(unidecode.unidecode(titulo.lower().replace(" ","-")))
    
    # Edita o conjunto de dados
    def edit_dataset(id, conn_id, titulo, freq_atualizacao, dia, schema, database, table, tipo_atualizacao, ultima_atualizacao, atualizacao_automatica, criar_metadados):
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        qry_upd_ds_info = ('update dataset set '
            'conn_id = :conn_id, '
           ' ds_name = :ds_name, '
           ' ds_upd_period = :ds_upd_period, '
           ' ds_upd_day =  :ds_upd_day, '
           ' ds_schema = :ds_schema, '
           ' ds_table = :ds_table, '
           ' ds_updt_type = :ds_updt_type, '
           ' ds_auto_updt = :ds_auto_updt, '
           ' ds_last_updt = :ds_last_updt, '
           ' ds_create_metadata = :ds_create_metadata '
           'where id = {}'.format(id))

        params = {
            'conn_id': conn_id,
            'ds_name': titulo,
            'ds_upd_period': freq_atualizacao,
            'ds_upd_day': dia,
            'ds_schema': schema,
            'ds_table': table,
            'ds_updt_type' : tipo_atualizacao,
            'ds_auto_updt': atualizacao_automatica,
            'ds_last_updt': ultima_atualizacao,
            'ds_create_metadata': criar_metadados
        }
        cursor.execute(qry_upd_ds_info, params)
        conn.commit()
        conn.close()

        if criar_metadados:
            database_credentials = Connection.get_single_conn(conn_id)
            Dataset.create_metadata_ckan(titulo)
    
    # Deleta conjunto de dados e, se houver, seu metadados
    def delete_dataset(id):
        conn = sqlite3.connect(DATABASE_PATH)
        # obtem o nome do conjunto de dados a fim de apagar o metadados após a exclusão
        qry_sel = ("select ds_name from dataset where id = {}".format(id))
        cursor = conn.execute(qry_sel)
        dataset_name = cursor.fetchall()
        print(dataset_name)

        # Apaga o conjunto de dados do banco de dados
        query_del = ("delete from dataset where id = {}".format(id))
        conn.execute(query_del)
        conn.commit()
        conn.close()

        # Localiza o metadados e,caso o encontre, apaga-o
        if os.path.exists("{}/{}.yaml".format(METADATAPATH,dataset_name[0][0].lower().replace(" ","-"))):
            Dataset.delete_metadata(dataset_name[0][0].lower().replace(" ","-"))

    ########################## BANCO DE DADOS ########################
    # Conecta-se ao banco de dados (OBS: Utilizar o database postgresql por enquanto. Não utilizar o oracle)
    def db_connect(driver, host_name, port_id, database, user_name, password):
        engine = create_engine('{}://{}:{}@{}:{}/{}'.format(driver, user_name,password,host_name,port_id,database))
        return engine.connect()

    # Consulta SQL para exportar informações da tabela ( OBS: A propriedade schema é ocional)
    def db_query(table, schema = ""):
        if schema != "":
            schema += "."
        return "select * from {}{}".format(schema,table)
    
    ######################## RESOURCE ############################
    # Extrai os dados do conjunto de dados no banco
    def data_extr(connection, dataset, datasetName):
        
        # Conexão e consulta ao banco de dados
        engine = Dataset.db_connect(connection[0][2], connection[0][3], connection[0][4], connection[0][5], connection[0][6], connection[0][7])
        query = Dataset.db_query(dataset[0][6], dataset[0][5])

        # Nomenclatura do arquivo de metadados ( também será utilizado em outras propriedades )
        metadataTitle = unidecode.unidecode(dataset[0][2].lower().replace(" ","-"))

        metadataName = "{}".format(
            metadataTitle # Remove os acentos e coloca traço no nome do arquivo yaml
        ) 

        return pd.read_sql_query(sql=text(query), con=engine)
        
    ######################## METADADOS ###########################
    # Cria o metadados do conjunto de dados com resource baixado
    def create_metadata(connection, dataset):
        # Conexão e consulta ao banco de dados
        engine = Dataset.db_connect(connection[0][2], connection[0][3], connection[0][4], connection[0][5], connection[0][6], connection[0][7])

        query = Dataset.db_query(dataset["ds_table"], dataset["ds_schema"])

        # Nomenclatura do arquivo de metadados ( também será utilizado em outras propriedades )
        metadataTitle = unidecode.unidecode(dataset["ds_name"].lower().replace(" ","-"))

        metadataName = "{}".format(
            metadataTitle # Remove os acentos e coloca traço no nome do arquivo yaml
            ) 

        # nome do resource ( arquivo .csv )
        resourceName = "{}-{}".format(
            unidecode.unidecode(dataset["ds_name"].lower().replace(" ","-")) , # Remove os acentos e coloca traço no nome do arquivo yaml
            datetime.date.today().year # Insere no nome do metadados o ano vigente
        )

        # Salvando os dados no arquivo csv
        df = pd.read_sql_query(sql=text(query), con=engine).to_csv('metadata/{}.csv'.format(resourceName), index=False)
        
        ###################################################################
        # Descrevendo o conjunto de dados extraído do banco de dados
        # Além de criar os metadados, será necessário atualizar as informações
        # por virem muito vagas, como a propriedade name
        resource = Resource.describe('metadata/{}.csv'.format(resourceName))
        resource.name = resourceName
        resource.title = resourceName
        resource.path = "{}.csv".format(resourceName)

        # Informações do pacote ( conjunto de dados )
        package = Package(
            title = dataset["ds_name"].lower().replace(" ","-"),
            description = 'Descrição a ser implementada no futuro'
        )

        package.add_resource(resource) # Adicionando o resource ao conjunto de dados ( pacote )

        # Salvando o pacote
        package.to_yaml('metadata/{}.yaml'.format(metadataName))

        # Removendo o arquivo extraído para a criação dos metadados
        os.remove('metadata/{}.csv'.format(resourceName))
         
    # Cria metadados com o resources do pacote no CKAN
    def create_metadata_ckan(datasetName):
        ckan_control = CkanControl()

        datasetNameConverted = unidecode.unidecode(datasetName.lower().replace(" ","-"))
        #package = Package(CKAN_URL, control=ckan_control)
        package = Package("{}/{}".format(CKAN_URL,datasetNameConverted), control=ckan_control)

        qte_resource_por_pacote = len(package.resources)

        ano_atual = datetime.date.today().year
        for resource in range(qte_resource_por_pacote):
            if str(ano_atual) in package.resources[resource].name and "csv" in package.resources[resource].name:
                resource_atual = package.resources[resource].name
                resource_atual_link = package.resources[resource].path
                resource_file_name = resource_atual_link[-(len(resource_atual_link)-resource_atual_link.rfind('/')-1):]

            
        url_resource = resource_atual_link
        wget.download(url_resource, METADATAPATH) # Baixando resource atual no CKAN

        ###################################################################
        # Descrevendo o conjunto de dados extraído do banco de dados
        # Além de criar os metadados, será necessário atualizar as informações
        # por virem muito vagas, como a propriedade name
        resource = Resource.describe('metadata/{}.csv'.format(resource_file_name.replace(".csv","")))
        resource.name = resource_file_name
        resource.title = resource_file_name
        resource.path = "{}.csv".format(resource_file_name.replace(".csv",""))

        # Informações do pacote ( conjunto de dados )
        package = Package(
            title = datasetName,
            description = 'Descrição a ser implementada no futuro'
        )

        package.add_resource(resource) # Adicionando o resource ao conjunto de dados ( pacote )

        # Salvando o pacote
        package.to_yaml('metadata/{}.yaml'.format(datasetNameConverted))

        # Removendo o arquivo extraído para a criação dos metadados
        os.remove('metadata/{}.csv'.format(resource_file_name.replace(".csv","")))

    # Remove o metadados do conjunto de dados removido
    def delete_metadata(titulo):
        os.remove(f'metadata/{titulo}.yaml')

    ######################## CONJUNTO DE DADOS ###########################
    # Cataloga o conjunto de dados ao CKAN - INCOMPLETO
    def send_to_ckan(package_name, file):
        return requests.post('{}/api/action/resource_create'.format(url),
            data={"package_id":package_name , "name":"teste2023"},
            headers={"Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2OTA0NjU4NjUsImp0aSI6IjBOQWVoOV9nM0hSZDJGWEFWWWMzdWlGUG02SGNyMDI4elJIdWZvZVg5aDA1SDd2WV9nMVdWM19BbzFYVXdhZE1fbUViN1d5ZlRDUjZtLW8tIn0.xKE9THd-o7_m6j0lCsNnJ5qBBlPOVu2_dESdB1c1eCc"},
            files=[('upload', open(file))]).status_code

    # Atualiza o conjunto de dados pelo resource, que será catalogado na plataforma CKAN
    def update_dataset(dataset):
        # recupera as informações da conexão a ser utilizada para extrair o resource
        database_credentials = Connection.get_single_conn(dataset[0][1])

        # Baixando arquivo no CKAN - TESTE
        datasetNameConverted = unidecode.unidecode(dataset[0][2].lower().replace(" ","-"))
        ckan_control = CkanControl()
        package = Package("{}/{}".format(CKAN_URL,datasetNameConverted), control=ckan_control)
        qte_resource_por_pacote = len(package.resources)
        ano_atual = datetime.date.today().year
        for resource in range(qte_resource_por_pacote):
            if str(ano_atual) in package.resources[resource].name and "csv" in package.resources[resource].name:
                resource_atual = package.resources[resource].name
                resource_atual_link = package.resources[resource].path
                resource_file_name = resource_atual_link[-(len(resource_atual_link)-resource_atual_link.rfind('/')-1):]
                print(resource_file_name)
        url_resource = resource_atual_link
        wget.download(url_resource, METADATAPATH) # Baixando resource atual no CKAN

        # Extrai o conjunto de dados no banco de dados
        db_extracted = Dataset.data_extr(database_credentials, dataset, resource_file_name)

        # Caso o conjunto de dados exija concatenação, essa funcionalidade será realizada
        if dataset[0][7] == 2:
            
            url_resource = resource_atual_link
            wget.download(url_resource, METADATAPATH) # Baixando resource atual no CKAN

            #Concatenação
            print(resource_file_name)
            print(db_extracted)
            df_1 = pd.read_csv('metadata/{}'.format(resource_file_name))
            df_2 = db_extracted

            # Concatena os dois arquivos csv
            df_final = pd.concat([df_1, df_2])

            # Salva o arquivo concatenado na pasta files
            df_final.to_csv('metadata/{}'.format(resource_file_name), index=False)
        else:
            db_extracted.to_csv('metadata/{}'.format(resource_file_name), index=False)

        # Extrai o pacote
        source = Package('metadata/{}.yaml'.format(unidecode.unidecode(dataset[0][2].lower().replace(" ","-"))))

        # Cria o pipeline do pacote
        pck_pipeline = Pipeline(steps=[
            steps.resource_transform(
                name = resource_file_name, # Nome do resource no CKAN
                steps=[
                    steps.table_normalize(),
                    steps.table_write(path="temp/files/{}".format(resource_file_name)), # Local onde o resource processado será armazenado
                ]
            )
        ])

        target = source.transform(pck_pipeline)

        # Removendo os arquivos csv usados para o pré-processamento
        #os.remove('metadata/{}.csv'.format(resource_file_name.replace(".csv","")))