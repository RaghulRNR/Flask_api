from flask import Flask,jsonify,request
import mysql.connector
app=Flask(__name__)

con=mysql.connector.connect(user='root',password='root',host='localhost')
cur=con.cursor()

app.route('/login', methods=['POST'])
def insert_user():



if __name__ =='__main__':
    app.run()