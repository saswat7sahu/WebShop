from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder="./templates")
app.secret_key = 'secret'
# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '$@$w@T@123'
app.config['MYSQL_DB'] = 'flask'

# Initialize MySQL
mysql = MySQL(app)