from flask import Flask

app = Flask(__name__)


@app.route('/age/<int:age>')
def age(age):
    return "Age=%d"%age;
@app.route('/home/<name>')
def home(name):
    return "Hello ,"+name;
def about():
    return "Hello ,This is about page"
app.add_url_rule('/about',"about",about)
if __name__ == "__main__":
    app.run(debug=True)