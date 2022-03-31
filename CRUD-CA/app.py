from flask import Flask, render_template, redirect, url_for, request,session
from flask_navigation import Navigation
from flask_mysqldb import MySQL
from mysql.connector import (connection)
import logging
import mysql.connector




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
  #error = None
  #if error allora settare error="messaggio errore"
  #e poi render_template + error
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        return render_template('login.html', error=error)

@app.route("/fishino")
def fishino():
    try:
      cnx = get_connection()
      cursor = cnx.cursor(dictionary=True)
      cursor.execute("SELECT * FROM fishino")
      out = []
      
      for row in cursor:
        #fihsino.py[key] = cursor
        out.append(row)
      logging.debug(f'fishino records: {out}')
      
      cursor.close()
      cnx.close()
    except e as err:
      logging.exception(e)
        
    return render_template('fishino.html')

    
@app.route("/navbar")
def navbar():
    return render_template('navbar.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host="10.20.5.40")
