from flask import Flask, render_template, redirect, url_for, request,session
from flask_navigation import Navigation
from flask_mysqldb import MySQL


from mysql.connector import (connection)

import mysql.connector
from mysql.connector import errorcode

try:
  cnx = mysql.connector.connect(user='root',password='',host='localhost',database='ca')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
    print("Test database connection worked!")
    cnx.close()


app = Flask(__name__)
app.secret_key = "lachiavepiusegretadelmondo"
nav = Navigation(app)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'ca'

mysql = MySQL(app)
nav.Bar('navbar',[
    nav.Item('Home', 'index'),
    nav.Item('Fishino', 'fishino'),
    nav.Item('Login', 'login')
])


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        return render_template('login.html')

@app.route("/fishino")
def fishino():
    return render_template('fishino.html')

    
@app.route("/navbar")
def navbar():
    return render_template('navbar.html')

if __name__ == '__main__':
    app.run()