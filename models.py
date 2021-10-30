from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Table, Integer
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import backref, relationship
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(30), nullable=False,unique=True)
    birth_date= db.Column(db.DateTime, nullable=False)
    number_id = db.Column(db.String(30), nullable=False,unique=True)
    country = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    occupation = db.Column(db.String(30), nullable=False)
    vaccinated = db.Column(db.Boolean, nullable=False)
    role = db.Column(db.Integer,default=False)
    is_active = db.Column(db.Boolean, default=True)
    payments = db.relationship('Payment',backref='user',lazy=True)

    def __repr__(self):
        return "<User %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email,
            'birth_date':self.birth_date,
            'number_id': self.number_id,
            'country': self.country,
            'city': self.city,
            'phone': self.phone,
            'occupation': self.occupation,
            'vaccinated': self.vaccinated,
            'role': self.role,
            'is_active': self.is_active
            #'payments': self.payments
        }

    def serialize_just_login(self):
        return {
            'email': self.email,
            'password': self.password
        }

#Enum class gender to be set in class Service 

class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    date_init = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime, nullable=False)
    age_start = db.Column(db.Integer, nullable=False)
    age_end = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(300), nullable=False)
    gender = db.Column(db.Integer,nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")

    def __repr__(self):
        return "<Service %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date_init': self.date_init,
            'date_end': self.date_end,
            'age_start': self.age_start,
            'age_end': self.age_end,
            'notes': self.notes,
            'gender': self.gender
        }

#Helper to made Many to Many Relationship with User and Document
docs = db.Table('docs',
    db.Column('document_id',db.Integer, db.ForeignKey('document.id')),
    db.Column('user_id',db.Integer, db.ForeignKey('user.id'))
)

class Document(db.Model):
    __tablename__ = 'document'
    id = db.Column(db.Integer, primary_key=True)
    doc_type = db.Column(db.Integer)
    doc_description= db.Column(db.String(20))
    image = db.Column(db.LargeBinary)
    users = db.relationship('User',secondary=docs,backref=db.backref('users',lazy=True))

    def __repr__(self):
        return "<Document %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'doc_type': self.doc_type,
            'doc_description': self.doc_description,
            'image': self.image
        }

class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    date= db.Column(db.DateTime)
    description= db.Column(db.String(150))
    image = db.Column(db.LargeBinary)
    person_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    reserve = db.relationship('Reserve', backref='reserve',uselist=False)

class Reserve(db.Model):
    __tablename__ = 'reserve'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    gender = db.Column(db.Integer,nullable=False)
    age = db.Column(db.Integer)
    notes= db.Column(db.String(300))
    date=db.Column(db.DateTime)
    payment_id = db.Column(db.Integer,db.ForeignKey('payment.id'))
 
