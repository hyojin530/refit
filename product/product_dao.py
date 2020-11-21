from connection.mysql_login import get_connection

#order by need, dict
def post_list():
    sql = '''select * from posts'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
    finally:
        if conn is not None: conn.close()
    
    return result

#dict
def post_detail(post_idx):
    sql = '''select * from posts where post_idx=%s'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, post_idx)
        result = cursor.fetchone()
    finally:
        if conn is not None: conn.close()
    
    return result