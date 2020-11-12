from user import user_dao
from flask import Blueprint, render_template, request, session, redirect, current_app, url_for
from werkzeug.utils import secure_filename
import datetime
import os

product_blue = Blueprint('product_blue', __name__)

@product_blue.route('/')
def main_page():
    html = render_template()    #add html
    return 'html'

#등록페이지

#상세페이지

#메인페이지

#구독