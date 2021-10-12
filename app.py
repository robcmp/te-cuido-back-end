from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:admin@localhost:5432/tecuido' 
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

@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    request.get_json(force=True)
    print(request.json)

    email = request.json.get("email", None)
    password = request.json.get("password", None)
    # Query your database for username and password
    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Usuario o contraseña invalida"}), 401
    # create a new token with the user id inside

    return jsonify({ "msg": "Sesión iniciada satisfactoriamente" }), 200

if __name__ == "__main__":
    app.run()
 