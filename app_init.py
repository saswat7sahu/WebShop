from flask import Flask
from flask_mysqldb import MySQL
import os
app = Flask(__name__, template_folder="./templates")
app.secret_key = os.getenv('SECRET_KEY', 'default_secret')
# Configure MySQL using environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'flask')
# Initialize MySQL
mysql = MySQL(app)