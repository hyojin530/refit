from connection.mysql_connect import get_connection
import pymysql


#input column 수정
def add_post(user_idx, title, description, tags, price, category, size, brand, gender, certificate, receipt, image_count):
    sql = '''insert into posts(user_idx, title, written_time, description, tags, price, category, size, brand, gender, certificate, receipt, image_count, post_like, sell_yn, comment_count)
             values(%s, %s, now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0, 0, 0)'''
    
    sql1 = '''select last_insert_id()'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (user_idx, title, description, tags, price, category, size, brand, gender, certificate, receipt, image_count))
        conn.commit()
        cursor.execute(sql1)
        result = cursor.fetchone()
    finally:
        if conn is not None: conn.close()
        
    return result[0]


def add_post_file(post_idx, file_type, location):
    sql = '''insert into post_file(post_idx, file_type, location)
             values (%s, %s, %s)'''
             
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (post_idx, file_type, location))
        conn.commit()
    finally:
        if conn is not None: conn.close()
    
    return 'OK'


#order by need, dict
def post_list(order_type):
    sql = '''select posts.post_idx, posts.user_idx, post_like, location
            from posts inner join post_file on posts.post_idx=post_file.post_idx
            where file_idx in (select min(file_idx) from post_file group by post_idx)'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if order_type == 0:
            sql += ' order by posts.post_idx desc'
            cursor.execute(sql)
        else:
            sql += ' order by post_like desc'
            cursor.execute(sql)
        
        result = cursor.fetchall()
    finally:
        if conn is not None: conn.close()
    
    if not result:
        return False
    
    data_list = []
    for row in result:
        temp_dict = {}
        temp_dict['post_idx'] = row[0]
        temp_dict['user_idx'] = row[1]
        temp_dict['post_like'] = row[2]
        temp_dict['img_url'] = row[3]
        data_list.append(temp_dict)
    print(data_list)
    return data_list

#한글 인코딩 생각해야됨
def post_detail(post_idx):
    sql = '''select post_idx, posts.user_idx, email, user_img, title, written_time, description, tags, price, category, size, brand, gender, certificate, receipt, post_like, sell_yn, comment_count 
             from posts inner join user on user.user_idx = posts.user_idx
             where post_idx=%s'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, post_idx)
        result = cursor.fetchone()
    finally:
        if conn is not None: conn.close()
    
    if not result:
        return False
    
    data = {}

    data['post_idx'] = result[0]
    data['user_idx'] = result[1]
    data['user_email'] = result[2]
    data['user_img'] = result[3]
    data['title'] = result[4]
    data['time'] = result[5]
    data['text'] = result[6]
    data['tags'] = result[7]
    data['price'] = result[8]
    data['category'] = result[9]
    data['size'] = result[10]
    data['brand'] = result[11]
    data['gender'] = result[12]
    data['certificate'] = result[13]
    data['receipt'] = result[14]
    data['post_like'] = result[15]
    data['sell_yn'] = result[16]
    data['comment_count'] = result[17]
    
    return data

def post_file_list(post_idx):
    sql = '''select location from post_file where post_idx=%s'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, post_idx)
        result = cursor.fetchall()
    finally:
        if conn is not None: conn.close()
        
    if not result:
        return False

    file_list = []
    
    for row in result:
        file_list.append(row[0])
    print(file_list)
    return file_list

def add_comment(post_idx, user_idx, text):
    sql = '''insert into comment (post_idx, user_idx, text, to_comment)
             values (%s, %s, %s, 0)'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (post_idx, user_idx, text))
        conn.commit()
    finally:
        if conn is not None: conn.close()
    
    return 'OK'

def update_comment_count(post_idx, comment_count):
    sql = '''update posts set comment_count=%s where post_idx=%s'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (comment_count, post_idx))
        conn.commit()
    finally:
        if conn is not None: conn.close()
    
    return 'OK'

def delete_comment(comment_idx):
    sql = '''delete from comment where comment_idx=%s'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, comment_idx)
        conn.commit()
    finally:
        if conn is not None: conn.close()
        
    return 'OK'

def post_comment(post_idx):
    sql = '''select comment_idx, post_idx, user_idx, text from comment
             where post_idx=%s order by comment_idx'''
             
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, post_idx)
        result = cursor.fetchall()
    finally:
        if conn is not None: conn.close()
    
    if not result:
        return False
    
    data_list = []
    for row in result:
        temp_dict = {}
        temp_dict['comment_idx'] = row[0]
        temp_dict['post_idx'] = row[1]
        temp_dict['user_idx'] = row[2]
        temp_dict['text'] = row[3]
        data_list.append(temp_dict)    
    print(data_list)
    return data_list

def check_user_like(user_idx, post_idx):
    sql = '''select * from like_posts where user_idx=%s and post_idx=%s'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (user_idx, post_idx))
        result = cursor.fetchone()
    finally:
        if conn is not None: conn.close()
    
    if not result:
        return False
        
    return True

def sub_post_list(user_idx):
    sql = '''select posts.post_idx, posts.user_idx, name, email, user_img, title, description, tags, post_like, location, comment_count 
             from posts inner join post_file on posts.post_idx=post_file.post_idx
             inner join user on user.user_idx=posts.user_idx
             where posts.user_idx in (select followed from user_follow where following=%s)
             and file_idx in (select min(file_idx) from post_file group by post_idx)
             order by posts.post_idx desc'''
             
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, user_idx)
        result = cursor.fetchall()
    finally:
        if conn is not None: conn.close()

    if not result:
        return False

    data_list = []
    for row in result:
        temp_dict = {}
        temp_dict['post_idx'] = row[0]
        temp_dict['user_idx'] = row[1]
        temp_dict['user_name'] = row[2]
        temp_dict['user_email'] = row[3]
        temp_dict['user_img'] = row[4]
        temp_dict['title'] = row[5]
        temp_dict['description'] = row[6]
        temp_dict['tags'] = row[7]
        temp_dict['post_like'] = row[8]
        temp_dict['img_url'] = row[9]
        temp_dict['comment_count'] = row[10]
        data_list.append(temp_dict)    
    print(data_list)
    return data_list    

def check_sub(following, followed):
    sql = '''select follow_idx from user_follow
             where following=%s and followed=%s'''
             
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (following, followed))
        result = cursor.fetchone()
    finally:
        if conn is not None: conn.close()
        
    if not result:
        return False
    
    return result[0]

def add_sub(following, followed):
    sql = '''insert into user_follow (following, followed)
             values (%s, %s)'''
             
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (following, followed))
        conn.commit()
    finally:
        if conn is not None: conn.close()
    
    return 'OK'

def delete_sub(following, followed):
    sql = '''delete from user_follow where following=%s and followed=%s'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (following, followed))
        conn.commit()
    finally:
        if conn is not None: conn.close()
        
    return 'OK'

#test, not in notion to
def get_wishlist(user_idx):
    sql = '''select posts.post_idx, posts.user_idx, name, email, user_img, title, description, tags, post_like, location
             from posts inner join post_file on posts.post_idx=post_file.post_idx
             inner join user on user.user_idx=posts.user_idx
             where posts.post_idx in (select post_idx from wishlist where user_idx=%s)
             and file_idx in (select min(file_idx) from post_file group by post_idx)
             order by posts.post_idx desc'''

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, user_idx)
        result = cursor.fetchall()
    finally:
        if conn is not None: conn.close()
    
    if not result:
        return False
    
    data_list = []
    for row in result:
        temp_dict = {}
        temp_dict['post_idx'] = row[0]
        temp_dict['user_idx'] = row[1]
        temp_dict['user_name'] = row[2]
        temp_dict['user_email'] = row[3]
        temp_dict['user_img'] = row[4]
        temp_dict['title'] = row[5]
        temp_dict['description'] = row[6]
        temp_dict['tags'] = row[7]
        temp_dict['post_like'] = row[8]
        temp_dict['img_url'] = row[9]
        data_list.append(temp_dict)    
    print(data_list)
    return data_list  

def check_wish(user_idx, post_idx):
    sql = '''select wish_idx from wishlist
             where user_idx=%s and post_idx=%s'''
             
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (user_idx, post_idx))
        result = cursor.fetchone()
    finally:
        if conn is not None: conn.close()
        
    if not result:
        return False
    
    return result[0]

def add_wish(user_idx, post_idx):
    sql = '''insert into wishlist (user_idx, post_idx)
             values (%s, %s)'''
             
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (user_idx, post_idx))
        conn.commit()
    finally:
        if conn is not None: conn.close()
    
    return 'OK'

def delete_wish(user_idx, post_idx):
    sql = '''delete from wishlist where user_idx=%s and post_idx=%s'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (user_idx, post_idx))
        conn.commit()
    finally:
        if conn is not None: conn.close()
        
    return 'OK'


def search_post(text):
    sql = '''select posts.post_idx, posts.user_idx, post_like, location 
             from posts inner join post_file on posts.post_idx = post_file.post_idx
             where file_idx in (select min(file_idx) from post_file group by post_idx)
             and description like '''+"'%%#"+text+"%%'"
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
    finally:
        if conn is not None: conn.close()
        
    if not result:
        return False
    
    data_list = []
    for row in result:
        temp_dict = {}
        temp_dict['post_idx'] = row[0]
        temp_dict['user_idx'] = row[1]
        temp_dict['post_like'] = row[2]
        temp_dict['img_url'] = row[3]
        data_list.append(temp_dict)
    print(data_list)
    return data_list

def pay_list(user_idx):
    sql = '''select posts.post_idx, user.user_idx, email, title, price, location
             from cart inner join posts on posts.post_idx = cart.post_idx
             inner join post_file on posts.post_idx = post_file.post_idx
             inner join user on posts.user_idx = user.user_idx
             where file_idx in (select min(file_idx) from post_file group by post_idx)
             and cart.user_idx = %s'''
             
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, user_idx)
        result = cursor.fetchall()
    finally:
        if conn is not None: conn.close()
        
    if not result:
        return False
    
    data_list = []
    for row in result:
        temp_dict = {}
        temp_dict['post_idx'] = row[0]
        temp_dict['uesr_idx'] = row[1]
        temp_dict['user_email'] = row[2]
        temp_dict['title'] = row[3]
        temp_dict['price'] = row[4]
        temp_dict['location'] = row[5]
        data_list.append(temp_dict)
    print(data_list)
    return data_list

def cart_list(user_idx):
    sql = '''select post_idx from cart where user_idx=%s'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, user_idx)
        result = cursor.fetchone()
    finally:
        if conn is not None: conn.close()
        
    if not result:
        return 1    
        
    return result[0]