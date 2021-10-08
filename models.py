from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, Enum,DateTime,Boolean
from sqlalchemy.orm import relationship
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    numberID = db.Column(db.String(30), nullable=False)
    country  = db.Column(db.String(20), nullable=False)
    city  = db.Column(db.String(20), nullable=False)
    phone  = db.Column(db.String(20), nullable=False)
    occupation  = db.Column(db.String(30), nullable=False)
    vaccinated  = db.Column(db.Boolean, nullable=False)
    occupation  = db.Column(db.String(30), nullable=False)
    user_type = db.Column(db.Integer)
    isActive = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return "<User %r>" % self.id
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastname': self.name,
            'password': self.password,
            'email': self.email,
            'isActive': self.isActive
        }
    def serialize_just_username(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Service(db.Model):
    __tablename__= 'service'
    id= db.Column(db.Integer, primary_key=True)
    date_init= db.Column(db.DateTime, nullable=False)
    date_end= db.Column(db.DateTime, nullable=False)
    age_start= db.Column(db.Integer, nullable=False)
    age_end= db.Column(db.Integer, nullable=False)
    notes= db.Column(db.String(300), nullable=False)
    gender= db.Column(db.Enum("Male", "Female"), nullable=False)
    user_id=Column(Integer, ForeignKey('user.id'))
    user = relationship("User")

    def __repr__(self):
        return "<Service %r>" % self.id
    def serialize(self):
        return {
            'id': self.id,
            'date_init': self.date_init,
            'date_end': self.date_end,
            'age_start': self.age_start,
            'age_end': self.age_end,
            'notes': self.notes
        }