from flask import Flask, session, app, request, render_template
from connection import mysql_info, mysql_connect
from exts import db

app = Flask(__name__, template_folder='view', static_url_path='', static_folder='static')
app.secret_key = 'horangsecrettt'
mysql = mysql_info.info

app.config['SECRET_KEY'] = 'horangsecrettt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+mysql['user']+':'+mysql['password']+'@'+mysql['host']+'/'+mysql['db']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

@app.route('/test')
def index():
    return 'this is index page, OK'


import product from product
import user from user

app.register_blueprint(product.product_blue)
app.register_blueprint(user.user_blue)

app.run(host='0.0.0.0', port=5000)