from .pp_2_data import interpretation_columns
from login_model.connection import connect
#from connection import connect  # local
import json

test_data = {"email": 'jovicab@gmail.com', "name": "dfghdf",
             "results": [0, 1, 0, 0, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]}


class InstrumentPP2:
    def __init__(self, input_data) -> None:
        self.input_data = input_data
        # self.input_data = json.dumps(input_data)
        self.user_email = self.input_data["email"]
        self.examinee_name = self.input_data["name"]
        self.examinee_results = self.input_data["results"]
        self.conn = connect()

    def save_results(self):
        """
        inserts upitnik result to db
        """

        conn = connect()
        cursor = conn.cursor()

        insert_data = (self.user_email, 'pp_2', self.examinee_name,
                       json.dumps(self.examinee_results))

        try:
            cursor.execute(
                "INSERT INTO test_results (user_email, test_code, examinee_name, result)"
                "VALUES (%s, %s, %s, %s)", insert_data)

            conn.commit()
            return None
        except Exception as e:
            print("An error occurred:", e)
        finally:
            conn.close()


class ResultsPP2:
    def __init__(self, user_email) -> None:
        self.conn = connect()
        self.user_email = user_email
        self.input_map = interpretation_columns

    def dt_to_dict(self):
        with self.conn as db:
            cursor = db.cursor()
            cursor.execute(
                f"SELECT * FROM test_results WHERE test_code = 'pp_2'")
            db_data = cursor.fetchall()
            data = [value[0:] for value in db_data]

            return data

    def raw_results(self):
        data = self.dt_to_dict()
        results = [[value[3], json.loads(value[4]), value[0]]
                   for value in data if value[1] == self.user_email]
        return results

    def intepretation_factor(self, input_data, factor):
        score = 0
        for i in self.input_map[factor]:
            score += input_data[i - 1]

        return score

    def display_results(self):
        data = self.raw_results()
        return [[value[0], self.intepretation_factor(value[1], 'PCR_TOT'), [self.intepretation_factor(value[1], 'PCR_DET'),self.intepretation_factor(value[1], 'PCR_ANT')]] for value in data]


# InstrumentPP2(test_data).save_results()
# print(ResultsPP2('jovicab@gmail.com').display_results())


