from connection.mysql_login import get_connection

def post_list(order):
    sql = '''select * from post_sell'''
    
    return 'OK'