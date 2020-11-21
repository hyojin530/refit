from user import user_dao
from flask import Blueprint, render_template, request, session, redirect, current_app, url_for
from werkzeug.utils import secure_filename
import datetime
import os
from product import product_dao
from datetime import datetime

product_blue = Blueprint('product_blue', __name__)

#메인페이지 1차
@product_blue.route('/')
def main_page():
    data_new = product_dao.post_list(0)
    data_like = product_dao.post_list(1)
    
    html = render_template('main.html', data_new=data_new, data_like=data_like)
    return html

#검색 get
@product_blue.route('/search', methods=['get'])
def search_posts():
    html = render_template('/search_result') #검색 결과 페이지
    return html

#등록페이지
@product_blue.route('/post')
def register_post():
    html = render_template('register.html') #필요한거 없을듯..? user 정보?

#상품 업로드 틀   
@product_blue.route('/upload_post', methods=['post'])
def upload_post():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 1
    
    #data받기
    post_dir = current_app.config['POST_FILE']
    title = 'hi'
    post_file = 'file'

    post_idx = product_dao.add_post(user_idx, title)
 
    f_name = datetime.datetime.now().strftime("%Y%m%d_")+'{post_idx}_'.format(post_idx=post_idx)+secure_filename(post_file.filename)
    f_location = os.path.join(post_dir,f_name)
    post_file.save(f_location)
    user_dao.add_post_file(post_idx, 1, f_location)    

    return 'OK'


#상세페이지
@product_blue.route('/post/post_id=<post_idx>', methods=['get'])
def post_detail(post_idx):
    detail = product_dao.post_detail(post_idx)
    html = render_template('detail.html', data=data)
    return html

#구독페이지 1차
@product_blue.route('/subscribe')
def subscribe_list():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 2
    
    post_list = product_dao.sub_post(user_idx)
    for post in post_list:
        if post['comment_count'] != 0:
            comments = product_dao.post_comment(post['post_idx'])
            post['comments'] = comments        
    html = render_template('subscribe.html', post_list=post_list) #user, 구독 리스트(이미지 등), 좋아요, 댓글 등
    return html
 
#구독추가와 취소를 동시에? 같은버튼?
@product_blue.route('/subscription_update')
def add_subscription():
    if 'user_idx' in session:
        user_idx = session['user_idx']

    return 'OK'

#구독취소

#위시리스트페이지
@product_blue.route('/wishlist')
def wishlist():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 2
        
    data = get_wishlist(user_idx)
    
    return data[0]

#위시리스트추가


#위시리스트취소