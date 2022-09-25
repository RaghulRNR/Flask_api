from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)
auth = HTTPBasicAuth()
swagger = Swagger(app)

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@auth.login_required
@swag_from("api_doc.yml")
@app.route('/tasksall/', methods=['GET'])
def index():
    return "Hello, {}!".format(auth.current_user())

if __name__ == '__main__':
    app.run()