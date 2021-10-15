from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:pa3jH8!FuDb8DU@localhost:5432/tecuido' 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['ENV'] = "development"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db.init_app(app)
Migrate(app, db)

@app.route('/')
def home():
    return jsonify('Creando Back-End Te-Cuido')

@app.route("/user", methods=["POST", "GET"])
@cross_origin()
def user():
    if request.method == "GET":
        user = User.query.all ()
        user = list(map(lambda x: x.serialize(), user))
        return jsonify(user)
        if user is not None:
            return jsonify(user.serialize())
    else:
        user = User()
        # request.get_json(force=True) 
        user.name = request.json.get("name")
        user.last_name = request.json.get("last_name")
        user.password = request.json.get("password")
        user.email = request.json.get("email")
        user.number_id = request.json.get("number_id")
        if User.query.filter_by(email=user.email).first():
            return jsonify({"msg": "Correo ya utilizado"}), 460
        if User.query.filter_by(number_id=user.number_id).first():
            return jsonify({"msg": "DNI ya utilizado"}), 461
        user.country = request.json.get("country")
        user.city = request.json.get("city")
        user.phone = request.json.get("phone")
        user.occupation = request.json.get("occupation")
        user.vaccinated = request.json.get("vaccinated")
        user.user_type = request.json.get("user_type")
        user.is_active = request.json.get("is_active")
        #user.payments = request.json.get("payments")
    
        db.session.add(user)
        db.session.commit()
        
    return jsonify(user.serialize()), 200


@app.route("/user/<int:id>", methods=["GET","POST"])
def userById(id):
    if request.method == "GET":
        if id is not None:
            user = User.query.get(id)
            if user is None:
                return jsonify('Missing id parameter in route'), 404
            else:
                return jsonify(user.serialize()), 200
        else:
            return jsonify('Missing id parameter in route'), 404
    else:
        user = User()
        user.name = request.json.get("name")
        user.last_name = request.json.get("last_name")
        user.password = request.json.get("password")
        user.email = request.json.get("email")
        user.number_id = request.json.get("number_id")
        user.country = request.json.get("country")
        user.city = request.json.get("city")
        user.phone = request.json.get("phone")
        user.occupation = request.json.get("occupation")
        user.vaccinated = request.json.get("vaccinated")
        user.user_type = request.json.get("user_type")
        user.is_active = request.json.get("is_active")
        #user.payments = request.json.get("payments")
        
        db.session.add(user)
        db.session.commit()

    return jsonify(user.serialize()), 200

@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    # request.get_json(force=True)
    # print(request.json)

    email = request.json.get("email", None)
    password = request.json.get("password", None)
    # Query your database for username and password
    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Usuario o contraseña invalida"}), 401
    # create a new token with the user id inside

    return jsonify(user.serialize()), 200

if __name__ == "__main__":
    app.run()
