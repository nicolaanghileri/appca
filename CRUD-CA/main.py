from flask import Flask, render_template, redirect, url_for, request,session
from flask_navigation import Navigation
from flask_mysqldb import MySQL

from mysql.connector import (connection)
import logging
import mysql.connector
from graphs import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mammamia'
nav = Navigation(app)
nav_admin = Navigation(app)

# MySQL configurations
def get_connection():
  try:
    cnx = mysql.connector.connect(user='root',password='',host='localhost',database='ca')
    return cnx
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
  else:
      print("Test database connection worked!")  
  

nav.Bar('navbar',[
    nav.Item('Home', 'index'),
    nav.Item('Fishino', 'fishino'),
    nav.Item('Login', 'login'),
])

nav_admin.Bar('navbar', [
  nav.Item('Home', 'index'),
  nav.Item('Fishino', 'fishino'),
  nav.Item('Add User', 'add_user'),
  nav.Item('Add Fishino', 'add_fishino'),
  nav.Item('Logout', 'logout')
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
    try:
      cnx = get_connection()
      cursor = cnx.cursor(dictionary=True)
      cursor.execute("SELECT * FROM fishino")
      fishinos = []
      
      for row in cursor:
        print(row)
        fishinos.append(row)
      logging.debug(f'fishino records: {fishinos}')
      
      cursor.close()
      cnx.close()
    except Exception as e:
      logging.exception(e)
    return render_template('fishino.html', fishino= fishinos)

@app.route("/grafici")
def get_datas_from_fishino():
  return render_template("graphics.html", graph_data_humidity = humidity(), graph_data_co2=co2())
  """
    f = str(fishino)
    try:
      cnx = get_connection()
      cursor = cnx.cursor(dictionary=True)
      cursor.execute("SELECT * FROM datas WHERE fishino_name='?'" , f)
      fishinos_datas = [] 
      for row in cursor:
        print(row)
        fishinos_datas.append(row)
        logging.debug(f"datas records: ")
        
      cursor.close()
      cnx.close()
    except Exception as e:
      logging.exception(e)
    return render_template("fishino.html", data=fishinos_datas)"""
    
@app.route('/add_user')
def add_user():
  return render_template('add_user.html')

@app.route('/add_fishino')
def add_fishino():
  return render_template('add_fishino.html')

@app.route('/logout')
def logout():
  return None

if __name__ == '__main__':
    app.debug = True
    app.run(host="localhost")
