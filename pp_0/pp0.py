from .pp_0_data import test_questions
from .pp_0_data import interpretation_columns
from .pp_0_data import interpretation
from .pp_0_data import personalities
from .connection import connect
from datetime import datetime, timedelta
import random
import string
import json


primer_results = ['jovicab@gmail.com', 'pp_0', '{"1":"A","2":"A","3":"A","4":"A","5":"A","6":"A","7":"A","8":"A","9":"A","10":"A","11":"A","12":"A","13":"A","14":"A","15":"A","16":"A","17":"A","18":"A","19":"A","20":"A","21":"A","22":"A","23":"A","24":"A","25":"A","26":"A","27":"A","28":"A","29":"A","30":"A","31":"A","32":"A","33":"A","34":"A","35":"A","36":"A","37":"A","38":"A","39":"A","40":"A","41":"A","42":"A","43":"A","44":"A","45":"A","46":"A","47":"A","48":"A","49":"A","50":"A","51":"A","52":"A","53":"A","54":"A","55":"A","56":"A","57":"A","58":"A","59":"A","60":"A","61":"A","62":"A","63":"A","64":"A","65":"A","66":"A","67":"A","68":"A","69":"A","70":"A"}']
xxx = ['jovicab@gmail.com', 'xxxxxxxxxxxx', '{"1":"A","2":"A","3":"A","4":"A","5":"A","6":"A","7":"A","8":"A","9":"A","10":"A","11":"A","12":"A","13":"A","14":"A","15":"A","16":"A","17":"A","18":"A","19":"A","20":"A","21":"A","22":"A","23":"A","24":"A","25":"A","26":"A","27":"A","28":"A","29":"A","30":"A","31":"A","32":"A","33":"A","34":"A","35":"A","36":"A","37":"A","38":"A","39":"A","40":"A","41":"A","42":"A","43":"A","44":"A","45":"A","46":"A","47":"A","48":"A","49":"A","50":"A","51":"A","52":"A","53":"A","54":"A","55":"A","56":"A","57":"A","58":"A","59":"A","60":"A","61":"A","62":"A","63":"A","64":"A","65":"A","66":"A","67":"A","68":"A","69":"A","70":"A"}', 'Vanja']
raw_data = {1: 'A', 2: 'A', 3: 'A', 4: 'A', 5: 'A', 6: 'A', 7: 'A', 8: 'A', 9: 'A', 10: 'A', 11: 'A', 12: 'A', 13: 'A', 14: 'A', 15: 'A', 16: 'A', 17: 'A', 18: 'A', 19: 'A', 20: 'A', 21: 'A', 22: 'A', 23: 'A', 24: 'A', 25: 'A', 26: 'A', 27: 'A', 28: 'A', 29: 'A', 30: 'A', 31: 'A', 32: 'A', 33: 'A', 34: 'A', 35: 'A', 36: 'A', 37: 'A',
            38: 'A', 39: 'A', 40: 'A', 41: 'A', 42: 'A', 43: 'A', 44: 'A', 45: 'A', 46: 'A', 47: 'A', 48: 'A', 49: 'A', 50: 'A', 51: 'A', 52: 'A', 53: 'A', 54: 'A', 55: 'A', 56: 'A', 57: 'A', 58: 'A', 59: 'A', 60: 'A', 61: 'A', 62: 'A', 63: 'A', 64: 'A', 65: 'A', 66: 'A', 67: 'A', 68: 'A', 69: 'A', 70: 'A'}


def question_answer(counter):
    return {'Q': test_questions[counter][0], 'A': test_questions[counter][1], 'B': test_questions[counter][2]}


class RandomURLPP0:
    def __init__(self, sender_username) -> None:
        self.conn = connect()
        self.url = ''
        self.sender_username = sender_username
        self.url_duration = 12

    def read_duration_settings(self):
        """
        read settings data for user [duration for generated urls]
        """
        conn = self.conn
        cursor = conn.cursor()

        # Check if the user exists in the table
        sql = "SELECT urlduration FROM login_count WHERE useremail = %s"
        cursor.execute(sql, (self.sender_username,))
        user = cursor.fetchone()

        return user[0]

    def generate_url(self):
        """
        generate new random URL and writes x hours to time of URL creation
        """
        random_str = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=8))
        url = "upitnik_" + random_str

        return url

    def save_url(self):
        """
        generate new random URL and writes x hours to time of URL creation
        """
        duration = self.read_duration_settings()
        now = datetime.now() + timedelta(hours=duration)

        url = self.generate_url()
        conn = self.conn
        c = conn.cursor()
        c.execute('INSERT INTO generated_url (random_url, expiration, sender_mail, test_code) VALUES (%s, %s, %s, %s)',
                  (url, now, str(self.sender_username), 'pp_0'))
        conn.commit()
        return url


class ResultsPP0:
    def __init__(self, usermail) -> None:
        self.usermail = usermail
        self.input_data = self.result_data()
        self.raw_data = raw_data
        self.input_map = interpretation_columns

    def result_data(self):
        """
        gets pp0 data from database, cleans data from other user results and converts dict values from str to int
        """

        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM test_results WHERE test_code = 'pp_0'")

        results = cursor.fetchall()

        display_results = []
        for i in results:
            if i[1] == self.usermail:
                result_dict = json.loads(i[4])
                display_results.append(
                    [i[0], i[3], {int(key): value for key, value in result_dict.items()}])
        return display_results

    def dimension_count(self, dimension_index):
        """
        counts number of answers by input_map
        """
        score = 0

        for i in self.input_map[dimension_index]:
            if self.raw_data[i] == 'A':
                score += 1

        return score

    def get_type(self):
        """
        retrieves personality type
        """
        mbti_profile = ''
        result_dict = {}

        # E/I
        dim_E = self.dimension_count('EI')
        dim_I = 10 - dim_E
        if dim_E < dim_I:
            mbti_profile = mbti_profile + 'I'
        else:
            mbti_profile = mbti_profile + 'E'

        ei = (round(dim_E/10, 2), round(1-dim_E/10, 2))

        # S/N
        dim_S = self.dimension_count('SN')
        dim_N = 20 - dim_S
        if dim_S < dim_N:
            mbti_profile = mbti_profile + 'N'
        else:
            mbti_profile = mbti_profile + 'S'

        sn = (round(dim_S/20, 2), round(1-dim_S/20, 2))

        # T/F
        dim_T = self.dimension_count('TF')
        dim_F = 20 - dim_T
        if dim_T < dim_F:
            mbti_profile = mbti_profile + 'F'
        else:
            mbti_profile = mbti_profile + 'T'

        tf = (round(dim_T/20, 2), round(1-dim_T/20, 2))

        # J/P
        dim_J = self.dimension_count('JP')
        dim_P = 20 - dim_J
        if dim_J < dim_P:
            mbti_profile = mbti_profile + 'P'
        else:
            mbti_profile = mbti_profile + 'J'

        jp = (round(dim_J/20, 2), round(1-dim_J/20, 2))

        result_dict = {
            'type': mbti_profile,
            'EI': ei,
            'SN': sn,
            'TF': tf,
            'JP': jp
        }

        return mbti_profile

    def result_page_data(self):
        """
        gathers list of results for table result view [[user1_name, user1_results], ...]
        """
        data = self.input_data
        output = []
        for i in range(len(data)):
            self.raw_data = data[i][2]
            output.append([data[i][0], data[i][1], self.get_type()])

        return output


class InterperationModalPP0:
    def __init__(self, db_id) -> None:
        self.db_id = db_id
        self.data = self.get_data()
        self.input_map = interpretation_columns
        self.intepretation = interpretation

    def get_data(self):
        """
        gets raw result data based on result id
        """
        conn = connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM test_results WHERE id = %s"
        cursor.execute(sql, (self.db_id,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        results = json.loads(results[0][4])
        results = {int(key): value for key, value in results.items()}
        return results

    def dimension_count(self, dimension_index):
        """
        counts number of answers by input_map
        """
        score = 0

        for i in self.input_map[dimension_index]:
            if self.data[i] == 'A':
                score += 1

        return score

    def get_type(self):
        mbti_profile = ''

        # E/I
        dim_E = self.dimension_count('EI')
        dim_I = 10 - dim_E
        if dim_E < dim_I:
            mbti_profile = mbti_profile + 'I'
        else:
            mbti_profile = mbti_profile + 'E'

        ei = (round(dim_E/10, 2), round(1-dim_E/10, 2))

        # S/N
        dim_S = self.dimension_count('SN')
        dim_N = 20 - dim_S
        if dim_S < dim_N:
            mbti_profile = mbti_profile + 'N'
        else:
            mbti_profile = mbti_profile + 'S'

        sn = (round(dim_S/20, 2), round(1-dim_S/20, 2))

        # T/F
        dim_T = self.dimension_count('TF')
        dim_F = 20 - dim_T
        if dim_T < dim_F:
            mbti_profile = mbti_profile + 'F'
        else:
            mbti_profile = mbti_profile + 'T'

        tf = (round(dim_T/20, 2), round(1-dim_T/20, 2))

        # J/P
        dim_J = self.dimension_count('JP')
        dim_P = 20 - dim_J
        if dim_J < dim_P:
            mbti_profile = mbti_profile + 'P'
        else:
            mbti_profile = mbti_profile + 'J'

        jp = (round(dim_J/20, 2), round(1-dim_J/20, 2))

        result_dict = {
            'type': mbti_profile,
            'EI': ei,
            'SN': sn,
            'TF': tf,
            'JP': jp
        }

        return result_dict

    def interpretation_modal(self):
        """
        gathers complete results for interpetation modal
        """
        type = self.get_type()
        for i in self.intepretation:
            if self.intepretation[i]['MBTI_code'] == type['type']:
                description = {'type': type['type'],
                               'score': [type['EI'], type['SN'], type['TF'], type['JP']],
                               'title': self.intepretation[i]['MBTI_personality_title'],
                               'description': self.intepretation[i]['MBTI_personality_description'][0],
                               'career': self.intepretation[i]['MBTI_personality_description'][1]
                               }
        return description


class InterpretationExamineePP0:
    def __init__(self, input_id) -> None:
        self.input_id = input_id
        self.type_data = self.result_data()
        self.input_map = interpretation_columns
        self.personalities = personalities
  
    def result_data(self):
        """
        get MBTI results where ID
        """
        conn = connect()
        cursor = conn.cursor()
        sql = "SELECT result FROM test_results WHERE id = %s"
        cursor.execute(sql, (self.input_id,))

        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None


    def examinee_dimension_count(self, dimension_index):
        """
        counts number of answers by input_map
        """
        score = 0
        data = json.loads((self.type_data))
        data = {int(key):value for key, value in data.items()}
        for i in self.input_map[dimension_index]:
            if data[i] == 'A':
                score += 1
        return score

    def examinee_get_type(self):
        
        mbti_profile = ''

        # E/I
        dim_E = self.examinee_dimension_count('EI')
        dim_I = 10 - dim_E
        if dim_E < dim_I:
            mbti_profile = mbti_profile + 'I'
        else:
            mbti_profile = mbti_profile + 'E'

        ei = (round(dim_E/10, 2), round(1-dim_E/10, 2))

        # S/N

        dim_S = self.examinee_dimension_count('SN')
        dim_N = 20 - dim_S
        if dim_S < dim_N:
            mbti_profile = mbti_profile + 'N'
        else:
            mbti_profile = mbti_profile + 'S'

        sn = (round(dim_S/20, 2), round(1-dim_S/20, 2))

        # T/F
        dim_T = self.examinee_dimension_count('TF')
        dim_F = 20 - dim_T
        if dim_T < dim_F:
            mbti_profile = mbti_profile + 'F'
        else:
            mbti_profile = mbti_profile + 'T'

        tf = (round(dim_T/20, 2), round(1-dim_T/20,2))

        # J/P
        dim_J = self.examinee_dimension_count('JP')
        dim_P = 20 - dim_J
        if dim_J < dim_P:
            mbti_profile = mbti_profile + 'P'
        else:
            mbti_profile = mbti_profile + 'J'

        jp = (round(dim_J/20, 2), round(1-dim_J/20, 2))

        result_dict = {
            'type': mbti_profile,
            'dimensions' : {
                'EI': ei,
                'SN': sn,
                'TF': tf,
                'JP': jp}
        }

        return result_dict

    def examinee_interpretation(self):
        interpretation_dict = self.examinee_get_type()
        type = interpretation_dict['type']
        for key,value in self.personalities.items():
            if key == type:
                interpretation_dict['title'] = value['title']
                interpretation_dict['description'] = value['description']
                interpretation_dict['career'] = value['career']
                interpretation_dict['strengths'] = value['strengths']
                interpretation_dict['weaknesses'] = value['weaknesses']
                interpretation_dict['rules'] = value['rules']
            
        return interpretation_dict


class ModelPP0:
    def __init__(self) -> None:
        pass

    def save_results(self, data):
        """
        saves results [user_mail, test_code, results, name of examinee] into MySQL db
        """
        conn = connect()
        cursor = conn.cursor()

        insert_data = (data[0], data[1], data[2], data[3])

        try:
            cursor.execute(
                "INSERT INTO test_results (user_email, test_code, examinee_name, result)"
                "VALUES (%s, %s, %s, %s)", insert_data)

            # Return the id of the inserted row
            inserted_id = cursor.lastrowid

            conn.commit()
            return inserted_id
        except Exception as e:
            print("An error occurred:", e)
        finally:
            conn.close()


class DeleteURLPP0:
    def __init__(self, url) -> None:
        self.conn = connect()
        self.url = url

    def delete_link(self):
        """
        after test is finished, radnom generated url is deleted from MySQL db
        """
        conn = self.conn
        cursor = conn.cursor()
        sql = "DELETE FROM generated_url WHERE random_url = %s"
        cursor.execute(sql, (self.url,))
        conn.commit()


# print(MBTIResults(xxx).get_type())
# print(PP0_model().display_basic_results('jovicab@gmail.com'))
#print(ModelPP0().save_results(primer_results))
# print(question_answer(5))
# print(MBTI_interpretation('ISTJ').end_interpetation())
# print(ResultsPP0("jovicab@gmail.com").result_page_data())
#print(InterperationModalPP0(93).interpretation_modal())
# xxx = {'email': 'jovicab@gmail.com', 'user': 'qqqqqqqqqqqqq', 'type': 'ESTJ', 'dimensions': [1.0, 1.0, 1.0, 1.0]}
# PP0_model().display_results('jovicab@gmail.com')
#rint(InterpretationExamineePP0(93).examinee_interpretation())