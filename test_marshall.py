from flask import Flask, jsonify,abort
from flask_restful import Api, Resource, fields, marshal_with, reqparse
from flask import make_response
from flask import request
app = Flask(__name__)
import mysql.connector


try:
    con=mysql.connector.connect(user='root',password='root',host='localhost',database='gym')
    cur=con.cursor()
except mysql.connector.Error as err:
    print(err)

resource_fields = {
    "name": fields.String,
    "phoneno": fields.String,
}

class TestAPI(Resource):
    @marshal_with(resource_fields)
    def get(self):
        sql = "select * from customers ;"
        cur.execute(sql)
        result = cur.fetchall()
        return result

api.add_resource(TestAPI, '/all','/all')


if __name__ == '__main__':
    app.run(debug=True)
    api=Api(app)


