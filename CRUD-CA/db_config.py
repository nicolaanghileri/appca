from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'adminca'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Password&1'
app.config['MYSQL_DATABASE_DB'] = 'ca'
app.config['MYSQL_DATABASE_HOST'] = '10.20.5.38'

mysql.init_app(app)
