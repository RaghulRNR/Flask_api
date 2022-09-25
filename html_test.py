from flask import Flask, request, render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import os
import pandas as pd

app = Flask(__name__)
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


@app.route('/login')
def my_form():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def my_form_post():
    text = request.form['uname']
    processed_text = text.upper()
    return processed_text

@app.route('/signup')
def singUp():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    name = request.form['uname']
    password=request.form['password']
    phoneno=request.form['phoneNumber']
    address=request.form['address']
    age=request.form['age']
    gender=request.form['gender']
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=name, password=hashed_password, admin=False,phoneno=phoneno,address=address,age=age,gender=gender)
    db.session.add(new_user)
    db.session.commit()

    return jsonify('message:success')

@app.route('/users', methods=['GET'])
def get_all_users():

    users = User.query.all()
    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['admin'] = user.admin
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['phoneno'] = user.phoneno
        user_data['address'] = user.address
        user_data['age'] = user.age
        user_data['gender'] = user.gender

        output.append(user_data)
    table = pd.DataFrame.from_dict(output)
    return render_template('table.html', tables=[table.to_html(classes='data')], titles=table.columns.values)


@app.route('/users')
def list_users():
    return render_template('table.html')

if __name__ =="__main__":
    app.run(debug=True)