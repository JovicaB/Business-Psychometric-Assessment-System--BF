from data.connection import mysql_connect
from data.pi_data import pi2_questions, pi2_interpretation_columns, pi2_short_interpretation, pi2_personalities_interpretation
from utils import DatabaseManager
import json


class PI2Questionnaire:
    @staticmethod
    def question_answer(counter):
        return {'Q': pi2_questions[counter][0], 'A': pi2_questions[counter][1], 'B': pi2_questions[counter][2]}


class InterpretationPI2:
    def __init__(self, user_identifier) -> None:
        self.conn = mysql_connect()
        self.user_identifier = user_identifier
        self.data = DatabaseManager(
            self.user_identifier, 'pi_2').read_results()

    def mbti_dimension_count(self, dimension_index, input_dict):  # OVDE SAM STAO
        """
        counts number of answers in a result dictionary using input_map; input_dict example = {1:"A", 2:"A", 3:"B"...}
        """
        input_map = pi2_interpretation_columns
        score = 0

        for i in input_map[dimension_index]:
            if input_dict[i] == 'A':
                score += 1
        return score

    def get_mbti_type(self, input_dict):
        """
        retrieves personality type
        """
        mbti_profile = ''
        result_dict = {}

        # E/I
        dim_E = self.mbti_dimension_count('EI', input_dict)
        dim_I = 10 - dim_E
        if dim_E < dim_I:
            mbti_profile = mbti_profile + 'I'
        else:
            mbti_profile = mbti_profile + 'E'

        ei = (round(dim_E/10, 2), round(1-dim_E/10, 2))

        # S/N
        dim_S = self.mbti_dimension_count('SN', input_dict)
        dim_N = 20 - dim_S
        if dim_S < dim_N:
            mbti_profile = mbti_profile + 'N'
        else:
            mbti_profile = mbti_profile + 'S'

        sn = (round(dim_S/20, 2), round(1-dim_S/20, 2))

        # T/F
        dim_T = self.mbti_dimension_count('TF', input_dict)
        dim_F = 20 - dim_T
        if dim_T < dim_F:
            mbti_profile = mbti_profile + 'F'
        else:
            mbti_profile = mbti_profile + 'T'

        tf = (round(dim_T/20, 2), round(1-dim_T/20, 2))

        # J/P
        dim_J = self.mbti_dimension_count('JP', input_dict)
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
    
    def clean_results(self):
        data = [json.loads(value['result']) for value in self.data.values()]
        names = [name['examinee_name'] for name in data]
        result_data = [value['result'] for value in data]
        result_data_int = [{int(k): v for k, v in d.items()} for d in result_data]
        merged_data = [{'examinee_name': name, 'result': result} for name, result in zip(names, result_data_int)]
        
        return merged_data


    def results(self):
        data = self.clean_results()
        names = [name['examinee_name'] for name in data]
        personality_type = [self.get_mbti_type(value['result'])['type'] for value in data]

        result = [[name, typ] for name, typ in zip(names, personality_type)]

        return result

    def short_interpretation(self, mbti_type):
        result = [value for value in pi2_short_interpretation.values() if value['MBTI_code'] == mbti_type]
        return result

    def detailed_interpretation(self, mbti_type):
        result = [value for key, value in pi2_personalities_interpretation.items() if key == mbti_type]
        return result


# print(PI2Questionnaire().question_answer(5))
# print(InterpretationPI2('jovicab@gmail.com').detailed_interpretation('ESTJ'))


