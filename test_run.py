from flask import Flask, jsonify,abort
from flask_restful import Api, Resource, fields, marshal_with, reqparse
from flask import make_response
from flask import request

from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec,APISpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
import json
import mysql.connector

app = Flask(__name__)  # Flask app instance initiated
api = Api(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Test Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'

    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

try:
    con=mysql.connector.connect(user='root',password='root',host='localhost',database='gym')
    cur=con.cursor(dictionary=True,buffered=True)
except mysql.connector.Error as err:
    print(err)

class AwesomeRequestSchema(Schema):
    name = fields.String(required=True, description="insert data",)
    phoneno=fields.String(required=True, description="insert data",)

class getapi(MethodResource,Resource):
    @doc(description='Get all data', tags=['with parameters'])
    def get(self,name):
        sql = "select * from customers where name='"+name+"';"
        cur.execute(sql)
        result=cur.fetchall()
        print(result)
        #result=dict(result)
        return jsonify(dict(enumerate(result)))


    @doc(description='My First GET Awesome API.', tags=['with parameters'])
    def delete(self, name):
        sql = "Delete from customers where name= '" + name + "';"
        cur.execute(sql)
        con.commit()
        return jsonify({'name': name + 'deleted from db'})


class testapi(MethodResource, Resource):
    #@app.route('/tasks/all', methods=['GET'])
    @doc(description='My First GET Awesome API.', tags=['without patameters'])
    def get(self):

        sql = "select * from customers ;"
        cur.execute(sql)
        result = cur.fetchall()
        print(result)
        return jsonify(dict(enumerate(result)))

    @use_kwargs(AwesomeRequestSchema, location=('json'))
    @doc(description='inserting value in api', tags=['without patameters'])
    def post(self, **kwargs):
        data = dict(kwargs)
        name = data['name']
        phone_no = data['phoneno']
        sql = "INSERT INTO customers (name,phoneno) VALUES (%s, %s)"
        val = (name, phone_no)
        result = cur.execute(sql, val)
        con.commit()
        return jsonify({'task': 'added'})



class putapi(MethodResource, Resource):
    #@app.route('/tasks/update/<name>',methods=['PUT'])
    @use_kwargs(AwesomeRequestSchema, location=('json'))
    @doc(description='inserting value in api', tags=['Test'])
    def put(self, **kwargs):
        #print(name)
        name=request.json['name']
        print(name)
        print(kwargs)
        #print(data)
        '''name_update = data['name']
        phone_no = request.json['phone_no']
        sql = "select * from customers where name='" + name + "';"
        cur.execute(sql)
        result=cur.fetchall()
        update_query = "update customers set name='" + name_update + "',phoneno=" + phone_no + " where name= '"+name+"';"
        cur.execute(update_query)
        con.commit()'''
        return {"name":"Updated"}



api.add_resource(testapi, '/testapi/getall/')
api.add_resource(getapi,'/test/get/<name>')
api.add_resource(putapi,'/test/put/<name>')

docs.register(testapi)
docs.register(getapi)
docs.register(putapi)


if __name__ == "__main__":

    app.run(debug=True)
