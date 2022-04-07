from flask import Flask, render_template, redirect, url_for, request,session
from flask_navigation import Navigation
from flask_mysqldb import MySQL
from mysql.connector import (connection)
import logging
import mysql.connector
from graphs import *



app = Flask(__name__)
app.secret_key = "lachiavepiusegretadelmondo"
nav = Navigation(app)

# MySQL configurations
def get_connection():
  try:
    cnx = mysql.connector.connect(user='adminca',password='Password&1',host='10.20.5.38',database='ca')
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
    nav.Item('Login', 'login')
])


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        return render_template('login.html', error=error)

@app.route("/fishino")
def fishino():
    fishinos = []
    try:
      cnx = get_connection()
      cursor = cnx.cursor(dictionary=True)
      cursor.execute("SELECT * FROM fishino")
  
      for row in cursor:
        print(row)
        fishinos.append(row)
      logging.debug(f'fishino records: {fishinos}')
      
      cursor.close()
      cnx.close()
    except Exception as e:
      logging.exception(e)
    return render_template('fishino.html', fishino= fishinos)

@app.route("/fishino/<fishino>")
def get_datas_from_fishino(fishino):

    fishinos_datas = []
    try:
      cnx = get_connection()
      cursor = cnx.cursor(prepared=True)  #prepared + dict non funziona (bug della libreria)
      statement = """SELECT * FROM datas WHERE fishino_name=%s"""
      params = (fishino,)
      cursor.execute(statement, params)
      
      for row in cursor:
        result = dict(zip(cursor.column_names, row))
        print(result)
        fishinos_datas.append(result)
      logging.debug(f"datas records: {fishinos_datas}")
        
      cursor.close()
      cnx.close()
    except Exception as e:
      logging.exception(e)
    return render_template("fishino.html", data=fishinos_datas)

if __name__ == '__main__':
    app.debug = True
    app.run(host="10.20.5.40")
