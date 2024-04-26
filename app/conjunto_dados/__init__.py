from flask import Blueprint


bp=Blueprint('conjunto_dados',__name__)

from app.conjunto_dados import routes