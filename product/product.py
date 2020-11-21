from user import user_dao
from flask import Blueprint, render_template, request, session, redirect, current_app, url_for
from werkzeug.utils import secure_filename
import datetime
import os
from product import product_dao

product_blue = Blueprint('product_blue', __name__)

#메인페이지
@product_blue.route('/')
def main_page():
    data = product_dao.post_list()
    html = render_template('', data=data)    #add html
    return 'html'

#검색페이지get

#등록페이지

#상품등록

#상세페이지
@product_blue.route('/post/post_id=<post_idx>', methods=['get'])
def post_detail(post_idx):
    detail = product_dao.post_detail(post_idx)
    html = render_template('', data=data)
    return html


#구독페이지

#구독추가

#구독취소

#위시리스트페이지

#위시리스트추가

#위시리스트취소