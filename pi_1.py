from data.connection import mysql_connect
from data.pi_data import pi1_factor_names, pi1_work_conditions_improvement_data
import heapq
import json
from utils import DatabaseManager


class InterpretationPI1:
    def __init__(self, user_identifier) -> None:
        self.conn = mysql_connect()
        self.user_identifier = user_identifier
        self.data = DatabaseManager(
            self.user_identifier, 'pi_1').read_results()

    def average_results(self):
        """
        returns average results for each job satisfaction factor [list of 20 averages]
        """
        data = [json.loads(data['result'])[0] for data in self.data.values()]
        averages = [round(sum(values) / len(values), 2)
                    for values in zip(*data)]
        return averages

    def descriptive_results(self):
        """
        returns job satisfaction improvement results from user [list of user suggestions]
        """
        return [json.loads(data['result'])[1] for data in self.data.values() if len(json.loads(data['result'])[1]) > 0]

    def result_interpretation(self):
        """
        count, max value, min value, data for interpretation page
        """

        data_count = len(self.data)
        averages = self.average_results()
        factors = pi1_factor_names

        max_values = heapq.nlargest(3, enumerate(averages), key=lambda x: x[1])
        max_factors = [(factors[index], value) for index, value in max_values]

        min_values = heapq.nsmallest(3, enumerate(averages), key=lambda x: x[1])
        min_factors = [(factors[index], value) for index, value in min_values]

        int_results = {
            'count results': data_count,
            'max score': max_factors,
            'min score': min_factors
        }

        return int_results

    def satisfaction_improvement_data(self):
        """
        returns improvement [list] data for 3 job satifaction factors with lowest score
        """
        min_results = [data[0] for data in self.result_interpretation()['min score']]
        pp1_improvement_data = {data:pi1_work_conditions_improvement_data[data] for data in min_results}
        return pp1_improvement_data


# print(InterpretationPI1('jovicab@gmail.com').average_results())
# print(InterpretationPI1('jovicab@gmail.com').descriptive_results())
# print(InterpretationPI1('jovicab@gmail.com').result_interpretation())
# print(InterpretationPI1('jovicab@gmail.com').satisfaction_improvement_data())
