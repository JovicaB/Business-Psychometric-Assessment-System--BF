from data.connection import mysql_connect
from datetime import datetime, timedelta
import json
import random
import string


# OK
class RandomURLGenerator:
    def generate_url(self):
        """
        Generates random URL
        """
        random_str = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=8))
        url = "upitnik_" + random_str
        return url


# OK
class URLDatabaseManager:
    def __init__(self, user_identifier, pi_code) -> None:
        """
        user_identifier = user mail, pi_code = psychological instrument code [pi_1, pi_2, ...]
        """
        self.user_identifier = user_identifier
        self.pi_code = pi_code
        self.conn = mysql_connect()
        self.url_duration = 12
        self.url = RandomURLGenerator().generate_url()

    def read_duration_settings(self):
        """
        read url duration from user settings
        """
        with self.conn as connection:
            cursor = connection.cursor()
            sql = "SELECT url_duration FROM login_count WHERE user_identifier = %s"
            cursor.execute(sql, (self.user_identifier,))
            user = cursor.fetchone()
        return user[0]

    def save_url(self):
        """
        Save URL and add x hours to URL duration
        """
        # duration_settings = self.read_duration_settings()
        duration_settings = 1
        url_duration = datetime.now() + timedelta(hours=duration_settings)

        try:
            with self.conn as connection:
                cursor = connection.cursor()
                sql = 'INSERT INTO generated_url (random_url, expiration, user_identifier, pi_code) VALUES (%s, %s, %s, %s)'
                values = (self.url, url_duration, str(
                    self.user_identifier), self.pi_code)
                cursor.execute(sql, values)
                self.conn.commit()
        except Exception as e:
            print(
                f"An error occurred while saving the URL to the database: {e}")
            return None

        return None


# OK
class DeleteURL:
    def __init__(self, url) -> None:
        self.conn = mysql_connect()
        self.url = url

    def delete_url(self):
        """
        deletes the generated URL after the examinee's assessment is finished
        """
        try:
            with self.conn as connection:
                cursor = connection.cursor()
                sql = "DELETE FROM generated_url WHERE random_url = %s"
                cursor.execute(sql, (self.url,))
                self.conn.commit()
        except Exception as e:
            print(
                f"An error occurred while saving the URL to the database: {e}")
            return None

        return None


class DatabaseManager:
    def __init__(self, user_identifier, pi_code) -> None:
        self.conn = mysql_connect()
        self.user_identifier = user_identifier
        self.pi_code = pi_code

    def read_results(self):
        """
        loads p.instrument results into a dictionary
        """

        with self.conn as connection:
            cursor = connection.cursor()
            sql = "SELECT * FROM results WHERE user_identifier = %s AND pi_code = %s"
            cursor.execute(sql, (self.user_identifier, self.pi_code, ))
            names = [keys[0] for keys in cursor.description][1:]

            data = {row[0]: dict(zip(names, row[1:]))
                    for row in cursor.fetchall()}

            return data

    def save_results(self, input_data):
        """
        saves p.instrument results into the database
        """

        json_data = json.dumps(input_data)
        insert_data = (self.user_identifier, self.pi_code, json_data)

        connection = self.conn
        cursor = connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO results (user_identifier, pi_code, result)"
                "VALUES (%s, %s, %s)", insert_data)

            connection.commit()
        except Exception as e:
            print("An error occurred:", e)
        finally:
            connection.close()


# print(URLDatabaseManager('jovicab@gmail.com', 'pi_1').read_duration_settings())
# URLDatabaseManager('jovicab@gmail.com', 'pi_1').save_url() OK
# DeleteURL('upitnik_w7heriuu').delete_url() OK

# DatabaseManager('jovicab@gmail.com', 'pi_1').save_results([[5, 4, 2, 2, 4, 4, 4, 4, 4, 4, 3, 2, 3, 4, 4, 3, 4, 4, 3, 4], "upitnik"]) OK
# print(DatabaseManager('jovicab@gmail.com', 'pi_1').read_results()