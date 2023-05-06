from datetime import datetime, timedelta
from login_model.connection import connect
# from connection import connect #local
import heapq
import json
import random
import string


class RandomURLPP1:
    def __init__(self, sender_username) -> None:
        self.conn = connect()
        self.url = ''
        self.sender_username = sender_username
        self.url_duration = 12

    def read_duration_settings(self):
        conn = self.conn
        cursor = conn.cursor()

        # Check if the user exists in the table
        sql = "SELECT urlduration FROM login_count WHERE useremail = %s"
        cursor.execute(sql, (self.sender_username,))
        user = cursor.fetchone()

        return user[0]

    def generate_url(self):
        """
        generate random URL
        """
        random_str = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=8))
        url = "upitnik_" + random_str
        return url

    def save_url(self):
        """
        save URL and writes x hours to time of URL creation
        """
        duration = self.read_duration_settings()
        now = datetime.now() + timedelta(hours=duration)

        url = self.generate_url()
        conn = self.conn
        c = conn.cursor()
        c.execute('INSERT INTO generated_url (random_url, expiration, sender_mail, test_code) VALUES (%s, %s, %s, %s)',
                  (url, now, str(self.sender_username), 'pp_1'))
        conn.commit()
        return url


class ResultsPP1:
    def __init__(self, username) -> None:
        self.conn = connect()
        self.username = username
        self.count = 0
        self.data = self.dt_to_dict()

    def dt_to_dict(self):
        """
        raw database data set to dictionary
        """

        with self.conn as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM test_results")
            names = [keys[0] for keys in cursor.description][1:]

            data = {row[0]: dict(zip(names, row[1:]))
                    for row in cursor.fetchall()}

            return data

    # OK 
    def extract_num_results(self):
        data = self.data
        self.count = len([value for value in data.values()
                         if value['user_email'] == self.username])

        return [json.loads(x['result'])[0] for x in data.values() if x['user_email'] == self.username and x['test_code'] == 'pp_1']

    def average_results(self):
        data = self.extract_num_results()
        integer_data = [[int(num) for num in sublist] for sublist in data]

        averages = [round(sum(values)/len(values), 2)
                    for values in zip(*integer_data)]

        return averages

    # OK
    def descriptive_results(self):
        data = self.data
        return [json.loads(x['result'])[1] for x in data.values() if x['user_email'] == self.username and x['user_email'] != '' and x['test_code'] == 'pp_1' and len(json.loads(x['result'])[1]) > 0]

    def get_factor_name(self, index):
        factor_names = [
            "Opterećenost poslom",
            "Ravnoteža posao / život",
            "Stabilnost posla",
            "Radni uslovi",
            "Autonomija rada i fleksibilnost posla",
            "Vrednovanje učinaka rada",
            "Raznovrsnost radnih zadataka",
            "Kompenzacija",
            "Unutar-kompanijska komunikacija",
            "Izazovi",
            "Stepen angažovanja ličnih kompetencija",
            "Napredovanje",
            "Odnos sa nadređenima",
            "Nivo stresa",
            "Odnos sa kolegama",
            "Pristup menadžmenta u rešavanju interpersonalnih konflikata",
            "Prilike za profesionalni razvoj",
            "Beneficije",
            "Kompetnetnost menadžmenta",
            "Osećaj pripadnosti",
        ]

        return factor_names[index]

    def get_interpretation(self):
        """
        count, max value, min value, data for interpretation page
        """

        raw_data = self.data
        average_data = self.average_results()

        count = 0
        for key, value in raw_data.items():
            if 'user_email' in value and value['user_email'] == self.username and value['test_code'] == 'pp_1':
                count += 1

        max_values = heapq.nlargest(
            3, enumerate(average_data), key=lambda x: x[1])
        max_factors = [(self.get_factor_name(index), value)
                       for index, value in max_values]

        min_values = heapq.nsmallest(
            3, enumerate(average_data), key=lambda x: x[1])
        min_factors = [(self.get_factor_name(index), value)
                       for index, value in min_values]

        int_results = [
            count,
            max_factors,
            min_factors
        ]

        return int_results


class UpdateDBModelPP1:
    def __init__(self, input_data) -> None:
        self.conn = connect()
        self.input_data = input_data

    def save_upitnik_data(self):
        """
        inserts upitnik result to upitnik db
        """

        upitnik_data = self.input_data
        result_data = json.dumps([upitnik_data['raw_results'], upitnik_data['suggestion']])
        insert_data = (upitnik_data['user_email'], 'pp_1', result_data)

        connection = self.conn
        cursor = connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO test_results (user_email, test_code, result)"
                "VALUES (%s, %s, %s)", insert_data)

            connection.commit()
        except Exception as e:
            print("An error occurred:", e)
        finally:
            connection.close()


class DeleteURLPP1:
    def __init__(self, url) -> None:
        self.conn = connect()
        self.url = url

    def delete_upitnik_link(self):
        conn = self.conn
        cursor = conn.cursor()
        sql = "DELETE FROM generated_url WHERE random_url = %s"
        cursor.execute(sql, (self.url,))
        conn.commit()


