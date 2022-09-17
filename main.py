from flask import Flask
from flask_restful import Api,Resource
names=  {"rahul":{"age": 23,"gender": "male"},
         "vasanth":{"age": 24,"gender": "male"}}

app=Flask(__name__)
api=Api(app)
class HelloWorld(Resource):
    def get(self,name):
        return names[name]


api.add_resource(HelloWorld,"/helloworld/<string:name>")
if __name__ == '__main__':
    app.run(debug=True)