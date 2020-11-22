from user import user_dao
from flask import Blueprint, render_template, request, session, redirect, current_app, url_for
from werkzeug.utils import secure_filename
import datetime
import os
from product import product_dao
from datetime import datetime

product_blue = Blueprint('product_blue', __name__)

#메인페이지 1차
@product_blue.route('/home')
def main_page():
    data_new = product_dao.post_list(0)
    data_like = product_dao.post_list(1)
    print(session)
    html = render_template('main.html', data_new=data_new, data_like=data_like)
    return html

#검색 get 얘기가 필요..
@product_blue.route('/search', methods=['get'])
def search_posts():
    html = render_template('/search_result') #검색 결과 페이지
    return html

#등록페이지 얘기가 필요..
@product_blue.route('/write_post')
def register_post():
    html = render_template('register.html')
    return html

#상품 업로드 틀   
@product_blue.route('/upload_post', methods=['post'])
def upload_post():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 1
    
    title = request.form['title']
    description_tags = request.form['description']
    price = request.form['price']
    category = request.form['category']
    size = request.form['size']
    brand = request.form['brand']
    certificate = request.form['certificate']
    receipt = request.form['receipt']
    file_list = request.file.get_list() #check
    img_count = len(file_list)
    
    post_dir = current_app.config['POST_FILE']

    post_idx = product_dao.add_post(user_idx, title, description, tags, price, category, size, brand, certificate, receipt)
    
    n=1
    for post_file in file_list:
        f_name = datetime.datetime.now().strftime("%Y%m%d_")+'{post_idx}_{num}'.format(post_idx=post_idx, num=n)+secure_filename(post_file.filename)
        f_location = os.path.join(post_dir,f_name)
        post_file.save(f_location)
        user_dao.add_post_file(post_idx, 1, f_location)
        n += 1

    return 'OK'

#상품 삭제?

#상세페이지 컬럼 정해야
@product_blue.route('/post/post_id=<post_idx>', methods=['get'])
def post_detail(post_idx):
    post_detail = product_dao.post_detail(post_idx)
    
    if post_detail['comment_count'] != 0:
        comments = product_dao.post_comment(post_idx)
        post_detail['comments'] = comments
    html = render_template('detail.html', data=post_detail)
    return html


@product_blue.route('/upload_comment', methods=['post'])
def upload_comment():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 2
    
    post_idx = request.form['post_idx']
    comment_text = request.form['text']
    comment_count = request.form['comment']
    
    product_dao.add_comment(post_idx, user_idx, comment_text)
    product_dao.update_comment_count(post_idx, comment_count)
    
    return 'OK'
    
#코멘트 삭제?

#구독페이지 1차
@product_blue.route('/subscribe')
def subscribe_list():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 2
    
    post_list = product_dao.sub_post_list(user_idx)
    
    if not post_list:
        html = render_template('subscribe.html', post_list=False)
        return html
    
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
    else:
        return 'NO'
    
    followed = request.form['user_idx'] #maybe get?
    
    checked_idx = product_dao.check_sub(user_idx, followed)
    
    if not checked_idx:
        product_dao.add_sub(user_idx, followed)
    else:
        product_dao.delete_sub(user_idx, followed)
    
    return 'OK'


#위시리스트페이지
@product_blue.route('/wishlist')
def wishlist():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 2
        
    data = product_dao.get_wishlist(user_idx)
    html = render_template('like.html', post_list=data)
    
    return html

#위시리스트
