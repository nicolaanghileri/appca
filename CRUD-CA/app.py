from flask import Flask, render_template, redirect, url_for, request,session
from flask_navigation import Navigation
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from mysql.connector import (connection)
import logging
import json
import mysql.connector
from datetime import date, datetime, timedelta
from graphs import *

app = Flask(__name__)
app.secret_key = "lachiavepiusegretadelmondo"
nav = Navigation(app)
nav_admin = Navigation(app)

# MySQL configurations
def get_connection():
  try:
    cnx = mysql.connector.connect(user='ControlloAmbient',password='apYv#C-wg*b7gn6f',host='ControlloAmbientale.mysql.pythonanywhere-services.com',database='ControlloAmbient$ca')
    logging.debug('connection established')
    return cnx
  except mysql.connector.Error as err:
    logging.exception('error during db connection')

nav.Bar('navbar',[
    nav.Item('Home', 'index'),
    nav.Item('Fishino', 'fishino'),
    nav.Item('Login', 'login')
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

bcryptObj = Bcrypt(app)
@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    uname = request.form['username']
    password = request.form['pwd']
    hash_password = bcryptObj.generate_password_hash(password)
    statement = "SELECT * FROM usr WHERE username =%s"
    cnx = get_connection()
    cur = cnx.cursor
    res = cur.execute(statement , uname)
    if res > 0:
      data = cur.fetchone()
      pwd = data['pwd']
      if bcryptObj.check_password_hash(pwd , hash_password):
        session["login"] = True
        print("You have logged in succesfully")
      else:
        print("Password does not match");
        return redirect("/login.html")
    else:
      print(f"Username  '{uname}' does not exists")
      return redirect("login.html")

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

def insert_data(n , h , b , no , c , t):
    try:
      cnx = get_connection()
      cursor = cnx.cursor()
      now = datetime.now()
      statement = """INSERT INTO data(data, fishino_name, humidity, brightness, noise,co2 ,temperature) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
      val = (now, n ,h , b, no, c , t )
      cursor.execute(statement, val)
      cursor.close()
      cnx.commit()
      cnx.close()
    except Exception as e:
      logging.exception(e)


def is_fishino(fishino_name):
  try:
    exist = False
    cnx = get_connection()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT name FROM fishino")
    for row in cursor:
      if(fishino_name == row["name"]):
          exist = True
    cursor.close()
    cnx.close()
  except Exception as e:
    logging.exception(e)
  return exist

@app.route("/fishino/data" , methods=['POST'])
def get_insert_data():
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if(content_type == 'application/json'):
            json = request.json
            name = json["name"]
            if(is_fishino(name)):
                humidity = json["humidity"]
                brigthness = json["brightness"]
                noise = json["noise"]
                co2 = json["co2"]
                temperature = json["temperature"]
                insert_data(name , humidity , brigthness , noise , co2 , temperature)
            else:
                print(f"fishino name '{name}' does not exist")
        else:
            print('invalid content type')
    else:
        print('Invalid Method request')
    return "200"


@app.route('/add_user')
def add_user():
  render_template(add_user.html)
  if request.method == 'POST':
    uname = request.form['username']
    pwd =  request.form['pwd']
    hash_pwd = bcryptObj.generate_password_hash(pwd)
    cnx =  get_connection()
    cur =  cnx.cursor()
    statement = 'INSERT INTO user(username , pwd) VALUES (%s,%s)'
    val = (uname , hash_pwd)
    cur.execute(statement, val)
  else:
    print("invalid request method")

@app.route('/add_fishino')
def add_fishino():
  return render_template('add_fishino.html')

@app.route('/logout')
def logout():
  session.clear()
  return render_template("index.html")



if __name__ == '__main__':
    app.debug = True
    app.run(host="10.20.5.40")