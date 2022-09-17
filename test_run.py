from flask import Flask, jsonify,abort
from flask_restful import Api, Resource, fields, marshal_with, reqparse
from flask import make_response
from flask import request
import json
app = Flask(__name__)
import mysql.connector


try:
    con=mysql.connector.connect(user='root',password='root',host='localhost',database='gym')
    cur=con.cursor(dictionary=True,buffered=True)
except mysql.connector.Error as err:
    print(err)


@app.route('/tasks/all', methods=['GET'])
#@marshal_with(resource_fields)
def get_all():

    sql = "select * from customers ;"
    cur.execute(sql)
    result = cur.fetchall()
    print(result)
    return jsonify(dict(enumerate(result)))


@app.route('/tasksByName/<name>', methods=['GET'])
def get_tasks(name):
    sql = "select * from customers where name='"+name+"';"
    cur.execute(sql)
    result=cur.fetchall()
    print(result)
    #result=dict(result)
    return jsonify(dict(enumerate(result)))

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/tasks/add', methods=['POST'])
def create_task():
    name=request.json['name']
    phone_no = request.json['phone_no']
    sql = "INSERT INTO customers (name,phoneno) VALUES (%s, %s)"
    val = (name, phone_no)
    result=cur.execute(sql, val)
    print(result)
    con.commit()
    return jsonify({'task': 'added'}), 201

@app.route('/tasks/update/<name>',methods=['PUT'])
def update(name):
    name_update = request.json['name']
    phone_no = request.json['phone_no']
    sql = "select * from customers where name='" + name + "';"
    cur.execute(sql)
    result=cur.fetchall()
    update_query = "update customers set name='" + name_update + "',phoneno=" + phone_no + " where name= '"+name+"';"
    cur.execute(update_query)
    con.commit()
    return {"name":"Updated"}


@app.route('/tasks/delete/<name>',methods=['Delete'])
def delete(name):
    sql="Delete from customers where name= '"+name+"';"
    cur.execute(sql)
    con.commit()
    return jsonify({'name':name+'deleted from db'})

if __name__ == '__main__':
    app.run(debug=True)