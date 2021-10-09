from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:ecomsur@localhost:5432/tecuido' 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['ENV'] = "development"

db.init_app(app)
Migrate(app, db)

@app.route('/')
def home():
    return jsonify('Creando Back-End Te-Cuido')

@app.route("/user", methods=["POST", "GET"])
def user():
    if request.method == "GET":
        user = User.query.all()
        user = list(map(lambda user: user.serialize(), user))
        if user is not None:
            return jsonify(user)
    else:
        user = User()
        user.name = request.json.get("name")
        user.lastname = request.json.get("lastname")
        user.password = request.json.get("password")
        user.email = request.json.get("email")
        user.numberID = request.json.get("numberID")
        user.country = request.json.get("country")
        user.city = request.json.get("city")
        user.phone = request.json.get("phone")
        user.occupation = request.json.get("occupation")
        user.vaccinated = request.json.get("vaccinated")
        user.user_type = request.json.get("user_type")
        user.isActive = request.json.get("isActive")
        #user.payments = request.json.get("payments")

        db.session.add(user)
        db.session.commit()

    return jsonify(user.serialize()), 200

if __name__ == "__main__":
    app.run()
