from login_model.connection import connect


class URLDuration:
    def __init__(self, user_mail) -> None:
        self.user_mail = user_mail
        self.connect = connect()

    def duration_text(self, input_duration):

        if input_duration == 1:
            return "1 čas"
        elif input_duration in [2, 3, 4]:
            return str(input_duration) + " časa"
        elif input_duration in range(5, 21):
            return str(input_duration) + " časova"
        elif input_duration == 21:
            return str(input_duration) + " čas"
        else:
            return str(input_duration) + " časa"

    def set_duration(self, input_duration):
        cursor = self.connect.cursor()
        sql = "UPDATE login_count SET urlduration = %s WHERE useremail = %s"

        cursor.execute(sql, (input_duration, self.user_mail))
        self.connect.commit()

        return self.duration_text(input_duration)

    def read_duration(self):
        cursor = self.connect.cursor()
        sql = "SELECT urlduration FROM login_count WHERE useremail = %s"
        cursor.execute(sql, (self.user_mail,))
        result = cursor.fetchone()

        return self.duration_text(result[0])
    
    def read_duration_int(self):
        cursor = self.conn.cursor()
        sql = "SELECT urlduration FROM login_count WHERE useremail = %s"
        cursor.execute(sql, (self.user_mail,))
        result = cursor.fetchone()

        return result[0]

class ResetResults:
    def __init__(self, user, test_code) -> None:
        self.user = user
        self.test_code = test_code
        self.connect = connect()

    def reset_results(self):
        cursor = self.connect.cursor()
        sql = "DELETE FROM test_results WHERE user_email = %s AND test_code = %s"
        cursor.execute(sql, (self.user, self.test_code, ))
        self.connect.commit()
    
