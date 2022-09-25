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

class postapi(MethodResource,Resource):
    #@app.route('/tasks/add', methods=['POST'])
    @use_kwargs(AwesomeRequestSchema, location=('json'))
    @doc(description='inserting value in api', tags=['postapi'])
    def post(self,**kwargs):
        data = dict(kwargs)
        #print(type(data))
        #print(data['api_type'])
        name = data['name']
        phone_no = data['phoneno']
        #name="qwert"
        #phone_no="1234"
        sql = "INSERT INTO customers (name,phoneno) VALUES (%s, %s)"
        val = (name, phone_no)
        result = cur.execute(sql, val)
        con.commit()
        return jsonify({'task': 'added'})

api.add_resource(postapi,'/test/post/')
docs.register(postapi)


if __name__ == "__main__":

    app.run(debug=True)