from flask import Flask
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__, template_folder="./templates")
app.secret_key = os.getenv('SECRET_KEY', 'default_secret')
print(os.getenv('MYSQL_PASSWORD', ''))
# Configure MySQL using environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'db')
print(app.config['MYSQL_HOST'])
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'rootpassword')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'flask')
print(app.config['MYSQL_PASSWORD'])
# Initialize MySQL
mysql = MySQL(app)
