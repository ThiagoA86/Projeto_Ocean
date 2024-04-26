from flask import Blueprint


bp=Blueprint('conversor',__name__)

from app.conversor import routes