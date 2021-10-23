import re
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from flask_bcrypt import Bcrypt



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:admin@localhost:5432/tecuido' 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['ENV'] = "development"
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["JWT_SECRET_KEY"] = 'super-secreta'
app.config["SECRET_KEY"] = "otra-super-secreta"

db.init_app(app)
Migrate(app, db)
cors = CORS(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

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
        user.role = request.json.get("role")
        user.is_active = request.json.get("is_active")
        #user.payments = request.json.get("payments")
    
        db.session.add(user)
        db.session.commit()
        
    return jsonify(user.serialize()), 200


@app.route("/user/<int:id>", methods=["GET","POST"])
@cross_origin()
def userById(id):
    if request.method == "GET":
        user = User.query.get(id)
        if user is None:
            return jsonify('Missing id parameter in route'), 404
        else:
            return jsonify(user.serialize()), 200
        
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
        user.role = request.json.get("role")
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

@app.route("/banuser/<int:id>", methods=["PUT"])
@cross_origin()
def banuser(id):
    if id is not None:
        user = User.query.filter_by(id=id).first()
        if user is None :
            return jsonify("Usuario no existe."), 404
            # user = User.query.filter_by(id=user.id).first()
        user.is_active = request.json.get("is_active")
        db.session.commit()

    return jsonify(user.serialize()), 200

@app.route("/edit_user/<int:id>", methods=["GET","POST"])
@cross_origin()
def edit_user(id):
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
        # request.get_json(force=True) 
        user.name = request.json.get("name")
        user.last_name = request.json.get("last_name")
        user.password = request.json.get("password")
        user.email = request.json.get("email")
        user.number_id = request.json.get("number_id")
        user.country = request.json.get("country")
        user.city = request.json.get("city")
        user.phone = request.json.get("phone")
        user.occupation = request.json.get("occupation")
        #user.vaccinated = request.json.get("vaccinated")
        #user.user_type = request.json.get("user_type")
        #user.is_active = request.json.get("is_active")
        #user.payments = request.json.get("payments")
    
        db.session.add(user)
        db.session.commit()
        
    return jsonify(user.serialize()), 200

@app.route("/register", methods=["POST"])
def register():
    name = request.json.get("name")
    last_name = request.json.get("last_name")
    password = request.json.get("password")
    birth_date = request.json.get("birth_date")
    email = request.json.get("email")
    number_id = request.json.get("number_id")
    country = request.json.get("country")
    city = request.json.get("city")
    phone = request.json.get("phone")
    occupation = request.json.get("occupation")
    vaccinated = request.json.get("vaccinated")
    role = request.json.get("role")
    is_active = request.json.get("is_active")
    #payments = request.json.get("payments")
    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User()
        user.name = name
        user.last_name = last_name
        #Validating password
        password_regex = '^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'
        if re.search(password_regex, password):
            password_hash = bcrypt.generate_password_hash(password)
            user.password = password_hash
        else:
            return jsonify({
                "msg": "Contraseña no válida"
            }), 400

        user.birth_date= birth_date
        #Validating email
        email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.search(email_regex, email):
            user.email = email
        else:
            return jsonify({
                "msg": "Correo electrónico no válido"
            }), 400
        user.number_id = number_id
        user.country = country
        user.city = city
        user.phone = phone
        user.occupation = occupation
        user.vaccinated = vaccinated
        user.role = role
        user.is_active = is_active
        #user.payments = request.json.get("payments")
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "msg": "User registered successfully"
        }), 200
    else:
        return jsonify({
            "msg": "User already exist"
        }), 400



if __name__ == "__main__":
    app.run()
 