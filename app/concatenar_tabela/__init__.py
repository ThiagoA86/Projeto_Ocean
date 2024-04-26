from flask import Blueprint


bp=Blueprint('concatenar_tabela',__name__)

from app.concatenar_tabela import routes