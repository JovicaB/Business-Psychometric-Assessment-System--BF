from data.connection import mysql_connect
from data.pi_data import pi3_interpretation_columns
from utils import DatabaseManager
import json


class InterpretationPI3:
    def __init__(self, user_identifier) -> None:
        self.conn = mysql_connect()
        self.user_identifier = user_identifier
        self.data = DatabaseManager(
            self.user_identifier, 'pi_3').read_results()
        
    def PCLR_score(self, input_data, factor):
        score = 0
        for i in pi3_interpretation_columns[factor]:
            score += input_data[i - 1]

        return score
        
    def results(self):
        data = [json.loads(value['result']) for value in self.data.values()]
        names = [value['examinee_name'] for value in data]
        results = [value['result'] for value in data]
        score = [self.PCLR_score(results[0], 'PCR_TOT'), self.PCLR_score(results[0], 'PCR_DET'), self.PCLR_score(results[0], 'PCR_ANT')]
        return score
    
data = [0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0]

print(InterpretationPI3('jovicab@gmail.com').results())

