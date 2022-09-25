from flask import Flask, jsonify
from flask_restful import  request

import mysql.connector

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)
auth = HTTPBasicAuth()

app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "specs": [
            {
                "version": "0.0.1",
                "title": "Gym Test API",
                "endpoint": 'v1_spec',
                "route": '/Swagger/v1/App',
            }
            ]
}
swagger = Swagger(app)

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


try:
    con=mysql.connector.connect(user='root',password='root',host='localhost',database='gym')
    cur=con.cursor(dictionary=True,buffered=True)
except mysql.connector.Error as err:
    print(err)
    cur.close()
    con.close()

@auth.login_required
@swag_from("api_doc.yml")
@app.route('/tasksall/', methods=['GET'])
def get_all():
    sql = "select * from customers ;"
    cur.execute(sql)
    result = cur.fetchall()
    return jsonify(dict(enumerate(result)))

@app.route('/tasksByName/<name>', methods=['GET'])
@swag_from("get_name.yml")
def get_tasks(name):
    sql = "select * from customers where name='"+name+"';"
    cur.execute(sql)
    result=cur.fetchall()
    return jsonify(dict(enumerate(result)))


@app.route('/tasks/add', methods=['POST'])
@swag_from("yml_post.yml")
def create_task():
    name=request.json['name']
    phone_no = request.json['phoneno']
    sql = "INSERT INTO customers (name,phoneno) VALUES (%s, %s)"
    val = (name, phone_no)
    cur.execute(sql, val)
    con.commit()
    return jsonify({'task': 'added'}), 201


@app.route('/tasks/update/<name>',methods=['PUT'])
@swag_from("yml_put.yml")
def update(name):
    name_update = request.json['name']
    phone_no = request.json['phoneno']
    sql = "select * from customers where name='" + name + "';"
    cur.execute(sql)
    cur.fetchall()
    update_query = "update customers set name='" + name_update + "',phoneno=" + phone_no + " where name= '"+name+"';"
    cur.execute(update_query)
    con.commit()
    return {"name":"Updated"}

@app.route('/tasks/delete/<name>',methods=['Delete'])
@swag_from("get_name.yml")
def delete(name):
    sql="Delete from customers where name= '"+name+"';"
    cur.execute(sql)
    con.commit()
    return jsonify({'name':name+'deleted from db'})


if __name__== "__main__":
    app.run(debug=True)