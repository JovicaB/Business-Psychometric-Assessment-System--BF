import MySQLdb

def mysql_connect():
    connection=MySQLdb.connect(
        password="",
        database="", 
        user="", 
        port=,
        host="",
        charset='utf8mb4'
    )
    return connection
