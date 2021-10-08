from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from models import db,User,Service
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:pa3jH8!FuDb8DU@localhost:5432/tecuido'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG']= False

db.init_app(app)
Migrate(app,db)
