import MySQLdb

def connect():
    connection=MySQLdb.connect(
        password="96RmNs51NSqsrBLewTu0",
        database="railway", 
        user="root", 
        port=7552,
        host="containers-us-west-14.railway.app",
        charset='utf8mb4'
    )
    return connection