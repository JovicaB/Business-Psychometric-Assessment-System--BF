from .connection import connect


class LoginDB:
    def __init__(self, user_mail) -> None:
        self.user_mail = user_mail

    def login_count(self):
        conn = connect()
        cursor = conn.cursor()

        # Check if the user exists in the table
        sql = "SELECT * FROM login_count WHERE useremail = %s"
        cursor.execute(sql, (self.user_mail,))
        user = cursor.fetchone()

        if user:
            # User exists, update the login_count value
            login_count = user[2] + 1
            sql = "UPDATE login_count SET count = %s WHERE useremail = %s"
            cursor.execute(sql, (login_count, self.user_mail))
        else:
            # User does not exist, insert a new row
            sql = "INSERT INTO login_count (useremail, count, urlduration) VALUES (%s, 1, 12)"
            cursor.execute(sql, (self.user_mail,))

        conn.commit()
        cursor.close()
        conn.close()
