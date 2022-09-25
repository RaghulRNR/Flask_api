from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)#sequence
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    phoneno=db.Column(db.String(80))
    address=db.Column(db.String(80))
    age=db.Column(db.String(80))
    gender=db.Column(db.String(80))

app.config['SECRET_KEY'] = 'thisissecret'
db_path = os.path.join(os.path.dirname(__file__), '.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db.create_all()