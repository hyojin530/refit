from user import user_dao
from flask import Blueprint, render_template, request, session, redirect, current_app, url_for
from werkzeug.utils import secure_filename
import datetime
import os

user_blue = Blueprint('user_blue', __name__)

#login page
@user_blue.route('/login')
def login():
    html = render_template('/login.html')
    return html

#join post
@user_blue.route('/user_join_pro', methods=['post'])
def user_join():
    return 'OK'

#login post
@user_blue.route('/user_login_pro', methods=['post'])
def user_login():
    return 'OK'

#logout post if not?
@user_blue.route('/user_logout_pro', methods=['post'])
def user_logout():
    return 'OK'

#mypage
@user_blue.route('/mypage', methods=['post'])
def mypage():
    html = render_template('mypage.html') #유저정보, 유저 포스트 정보, 판매유무 등

#장바구니
@user_blue.route('/cart', methods=['post'])
def shopping_cart():
    html = render_template('shoppingcart.html') #장바구니 리스트 및 정보

#좋아요페이지

#결제페이지