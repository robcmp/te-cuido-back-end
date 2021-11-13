import re
from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import Payment, Service, db, User, Reserve
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
import mercadopago

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
mail = Mail(app)


# MAIL CONFIG
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pruebatecuido1@gmail.com'
app.config['MAIL_PASSWORD'] = 'Hola123.'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

sdk = mercadopago.SDK(
    "TEST-3228634650216916-111223-64bf0d1b49b876baaeea234ac0159d43-287091146")


@app.route('/')
def home():
    return jsonify('Creating Back-End Te-Cuido')


@app.route("/user", methods=["POST", "GET"])
@cross_origin()
def user():
    if request.method == "GET":
        user = User.query.all()
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
            return jsonify({"msg": "Email already used"}), 404
        if User.query.filter_by(number_id=user.number_id).first():
            return jsonify({"msg": "DNI already used"}), 404
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


@app.route("/user/<int:id>", methods=["GET", "POST"])
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
    if password == "":
        return jsonify({
            "msg": "Invalid password or password field is empty"
        }), 400

    if email == "":
        return jsonify({
            "msg": "Invalid email or email field is empty"
        }), 400

    # Query your database for username and password
    user = User.query.filter_by(email=email).first()

    if user is None:
        # the user was not found on the database
        return jsonify({
            "msg": "user doesn't exist"
        }), 401
    elif bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.email)
        return jsonify({
            "msg": "Successful login",
            "access_token": access_token,
            "user": user.serialize()
        }), 200
    else:
        return jsonify({
            "msg": "Incorrect access credentials"
        }), 400
    # create a new token with the user id inside

    # return jsonify(user.serialize()), 200


@app.route("/me", methods=["POST"])
@jwt_required()
def me():
    current_user = get_jwt_identity()
    current_user_token_expires = get_jwt()["exp"]
    return jsonify({
        "current_user": current_user,
        "current_user_token_expires": datetime.fromtimestamp(current_user_token_expires)
    }), 200


@app.route("/banuser/<int:id>", methods=["PUT"])
@cross_origin()
def banuser(id):
    if id is not None:
        user = User.query.filter_by(id=id).first()
        if user is None:
            return jsonify({
                "msg": "User doesn't exist"
            }), 400
        elif User.query.filter_by(id=id, is_active=False).first():
            return jsonify("User already banned"), 400
            # user = User.query.filter_by(id=user.id).first()
        user.is_active = request.json.get("is_active")
        db.session.commit()

    return jsonify(user.serialize()), 200


@app.route("/unbanuser/<int:id>", methods=["PUT"])
@cross_origin()
def unbanuser(id):
    if id is not None:
        user = User.query.filter_by(id=id).first()
        if user is None:
            return jsonify({
                "msg": "User doesn't exist"
            }), 400
        elif User.query.filter_by(id=id, is_active=True).first():
            return jsonify({
                "msg": "User already unbanned"
            }), 400
            # user = User.query.filter_by(id=user.id).first()
        user.is_active = request.json.get("is_active")
        db.session.commit()

    return jsonify(user.serialize()), 200


@app.route("/edit_user/<int:id>", methods=["GET", "POST"])
@cross_origin()
def edit_user(id):
    if request.method == "GET":
        if id is not None:
            user = User.query.get(id)
            if user is None:
                return jsonify('Missing id parameter in route'), 400
            else:
                return jsonify(user.serialize()), 200
        else:
            return jsonify('Missing id parameter in route'), 400
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

        db.session.add(user)
        db.session.commit()

    return jsonify(user.serialize()), 200


@app.route("/register", methods=["POST"])
@cross_origin()
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
        # Validating password
        password_regex = '^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'
        if re.search(password_regex, password):
            password_hash = bcrypt.generate_password_hash(
                password).decode('utf-8')
            user.password = password_hash
        else:
            return jsonify({
                "msg": "Invalid password"
            }), 400

        user.birth_date = birth_date
        # Validating email
        email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.search(email_regex, email):
            user.email = email
        else:
            return jsonify({
                "msg": "Invalid email"
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


@app.route("/delete_user/<id>", methods=["DELETE"])
@cross_origin()
def delete_user(id):
    if id is not None:
        user = User.query.get(id)
        if user is None:
            return jsonify({
                "msg": "User doesn't exist."
            }), 404
        db.session.delete(user)
        db.session.commit()

    return jsonify({
        "msg": "User deleted"
    }), 200


@app.route("/update_user/<int:id>", methods=["PUT"])
@cross_origin()
def update_user(id):
    if id is not None:
        user = User.query.filter_by(id=id).first()
        if user is None:
            return jsonify("User doesn't exist."), 404

        user.name = request.json.get("name")
        user.last_name = request.json.get("last_name")
        user.email = request.json.get("email")
        # Validating email (REVISARLOS)
        email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.search(email_regex, user.email):
            email = user.email
            user.email = email
        else:
            return jsonify({
                "msg": "invalid email"
            }), 400
        user.country = request.json.get("country")
        user.city = request.json.get("city")
        user.phone = request.json.get("phone")
        user.occupation = request.json.get("occupation")
        #user.payments = request.json.get("payments")

        db.session.add(user)
        db.session.commit()

    return jsonify(user.serialize()), 200


@app.route("/services/<int:id>", methods=["POST", "GET"])
@cross_origin()
def services(id):
    if request.method == "GET":
        user = User.query.filter_by(id=id).first()
        if user is None:
            return jsonify("User doesn't exist"), 404
        if id is not None:
            service = Service.query.filter_by(user_id=id)
            service = list(map(lambda x: x.serialize(), service))
            if service is None:
                return jsonify({"msg": "There are no services for this user"}), 404
            else:
                return jsonify(service), 200
        else:
            return jsonify({"msg": "Missing id parameter"}), 404
    else:
        if id is not None:
            user = User.query.filter_by(id=id).first()
            if user is None:
                return jsonify("User doesn't exist"), 404
            service = Service()
            service.date_init = request.json.get("date_init")
            service.date_end = request.json.get("date_end")
            service.age_start = request.json.get("age_start")
            service.age_end = request.json.get("age_end")
            service.notes = request.json.get("notes")
            service.gender = request.json.get("gender")
            service.price = request.json.get("price")
            service.user_id = id

            db.session.add(service)
            db.session.commit()

        return jsonify(service.serialize()), 200


@app.route("/delete_publication/<int:id>", methods=["DELETE"])
@cross_origin()
def delete_publication(id):
    if id is not None:
        service = Service.query.get(id)
        if service is None:
            return jsonify({
                "msg": "Service doesn't exist."
            }), 404
        db.session.delete(service)
        db.session.commit()

    return jsonify({
        "msg": "Service deleted"
    }), 200


@app.route("/list_services", methods=["GET"])
@cross_origin()
def list_services():
    if request.method == "GET":
        services = Service.query.all()
        if services is None:
            return jsonify("services doesn't exist"), 404
        services = list(map(lambda x: x.serialize(), services))
        return jsonify(services), 200


@app.route("/service_history/<int:user_id>", methods=["GET"])
@cross_origin()
def service_history(user_id):
    if request.method == "GET":
        services = Service.query.filter_by(user_id=user_id).all()
        if services is None:
            return jsonify("services history doesn't exist", 404)
        services = list(map(lambda x: x.serialize(), services))
        return jsonify(services),200


@app.route("/delete_services_by_id/<int:id>", methods=["DELETE"])
@cross_origin()
def delete_servicios_by_id(id):
    if id is not None:
        service = Service.query.get(id)
        if service is None:
            return jsonify({
                "msg": "Service doesn't exist."
            }), 404
        db.session.delete(service)
        db.session.commit()

    return jsonify({
        "msg": "Service deleted"
    }), 200


@app.route("/reserve/<int:id>", methods=["GET", "POST"])
@cross_origin()
def reserve(id):
    if request.method == "GET":
        reserve = Reserve.query.filter_by(id=id).first()
        if reserve is None:
            return jsonify("User doesn't exist"), 404
        if id is not None:
            reserve = Reserve.query.filter_by(user_id=id)
            reserve = list(map(lambda x: x.serialize(), reserve))
            if reserve is None:
                return jsonify({"msg": "There are no services for this user"}), 404
            else:
                return jsonify(reserve), 200
        else:
            return jsonify({"msg": "Missing id parameter"}), 404

    else:
        if id is not None:
            service = Service.query.filter_by(id=id).first()
            if service is None:
                return jsonify("Service doesn't exist"), 404
            service_date_start = service.date_init
            service_date_end = service.date_end
            service.is_reserved = True
            reserve = Reserve()
            reserve.name = request.json.get("name")
            reserve.gender = request.json.get("gender")
            reserve.age = request.json.get("age")
            reserve.notes = request.json.get("notes")
            reserve.date_start = service_date_start
            reserve.date_end = service_date_end
            reserve.carer_id = request.json.get("carer_id")
            reserve.client_id = request.json.get("client_id")
            reserve.status = request.json.get("status")
            reserve.service_id = id
            db.session.add(reserve)
            db.session.commit()

        return jsonify(reserve.serialize()), 200


@app.route('/reserved_service/<int:id>', methods=["GET", "POST"])
@cross_origin()
def reserved_service(id):
    if request.method == "GET":

        reserve = Reserve.query.filter_by(
            carer_id=id, status='RESERVED').all()
        if reserve is None:
            return jsonify({"msg", "Services doesn't exist"}), 404
        reserves = list(map(lambda x: x.serialize(), reserve))
        return jsonify(reserves), 200
    else:
        if id is not None:
            service = Service.query.filter_by(id=id, is_reserved=True).all()


@app.route('/reservations/carer/<int:id>', methods=["GET", "POST"])
@cross_origin()
def reservations_carer(id):
    if request.method == "GET":

        reserve = Reserve.query.filter_by(carer_id=id).all()
        if reserve is None:
            return jsonify({"msg", "Services doesn't exist"}), 404
        reservations = list(map(lambda x: x.serialize(), reserve))
        return jsonify(reservations), 200
    else:
        if id is not None:
            service = Service.query.filter_by(id=id, is_reserved=True).all()


@app.route('/reservations/client/<int:id>', methods=["GET", "POST"])
@cross_origin()
def reservations_client(id):
    if request.method == "GET":
        reserve = Reserve.query.filter_by(
            client_id=id, status="CONFIRMED").all()
        if reserve is None:
            return jsonify({"msg", "Services doesn't exist"}), 404
        reservations = list(map(lambda x: x.serialize(), reserve))
        return jsonify(reservations), 200
    else:
        if id is not None:
            service = Service.query.filter_by(id=id, is_reserved=True).all()


@app.route("/reserve_confirmation/<int:id>", methods=["PUT"])
@cross_origin()
def reserve_confirmation(id):
    if id is not None:
        reserve = Reserve.query.filter_by(id=id).first()
        if reserve is None:
            return jsonify({
                "msg": "Reserve doesn't exist"
            }), 400
        elif Reserve.query.filter_by(id=id, status="CONFIRMED").first():
            return jsonify("Reservation already done"), 400
        reserve.status = "CONFIRMED"
        subject = "Confirmacion de Reserva"
        body = "Reservacion confirmada"
        msg = Message(
            body=body,
            sender='pruebatecuido1@gmail.com',
            recipients=['roberto.cmp16@gmail.com'],
            subject=subject
        )
        mail.send(msg)

    db.session.commit()
    return jsonify({"reserve": reserve.serialize(), "msg": "mail sent"}), 200


@app.route("/reserve_rejection/<int:id>", methods=["PUT"])
@cross_origin()
def reserve_rejection(id):
    if id is not None:
        reserve = Reserve.query.filter_by(id=id).first()
        if reserve is None:
            return jsonify({
                "msg": "Reserve doesn't exist"
            }), 400
        elif Reserve.query.filter_by(id=id, status="REJECTED").first():
            return jsonify({
                "msg": "Reserve was already rejected"
            }), 400
            # user = User.query.filter_by(id=user.id).first()
        reserve.status = "REJECTED"
        subject = "Reservacion Rechazada"
        body = "Reservacion rechazada"
        msg = Message(
            body=body,
            sender='pruebatecuido1@gmail.com',
            recipients=['roberto.cmp16@gmail.com'],
            subject=subject
        )
        mail.send(msg)

        db.session.commit()

        return jsonify({"reserve": reserve.serialize(), "msg": "mail sent"}), 200

    @app.route("/payment/<int:id>", methods=["POST"])
    @cross_origin()
    def payment(id):
        if id is not None:
            reserve = Reserve.query.filter_by(id=id).first()

            if reserve is None:
                return jsonify({
                    "msg": "Reserve doesn't exist"
                }), 400

            payment = Payment()
            payment_name = request.json.get("name")
            payment_description = request.json.get("description")
            payment_person_id = request.json.get("person_id")

            payment.name = payment_name
            payment.date = datetime.now()
            payment.description = payment_description
            payment.person_id = payment_person_id
            payment.reserve = id
            db.session.add(payment)
            preference_data = {
                "items": [
                    {
                        "title": payment_name,
                        "quantity": 1,
                        "unit_price": 75
                    }
                ]
            }
            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]
            print(preference)
            db.session.commit()

            return jsonify("OK"), 200


if __name__ == "__main__":
    app.run()
