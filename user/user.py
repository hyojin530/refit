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

@user_blue.route('/user_join_pro', methods=['post'])
def user_join():
    return 'OK'

@user_blue.route('/user_login_pro', methods=['post'])
def user_login():
    return 'OK'

@user_blue.route('/user_logout_pro', methods=['post'])
def user_logout():
    return 'OK'

#mypage

#장바구니

#좋아요

#결제페이지

#로그인페이지