from data_frame_utils import *
from correlation_utils import *
import pandas
import numpy
import math
from scipy import stats
import matplotlib.pyplot as plotter

__author__ = 'michal-witkowski'


class DataAnalyser:

    def __init__(self, path):
        self.path = path
        self.data_frame = pandas.read_csv(path, sep=',')

    def prepare_data(self):
        self._cleanup_frame()
        self._add_new_variables()

    def answer_the_questions(self):
        self._answer_first_question()
        self._answer_second_question()
        self._answer_third_question()

    def prepare_data_for_exploration(self):
        pass

    def _cleanup_frame(self):
        self.data_frame.requestTime = pandas.to_numeric(self.data_frame.requestTime, errors='coerce')

    def _add_new_variables(self):
        self.data_frame['timestampDiff'] = self.data_frame['browser_timestamp'].sub(self.data_frame['timestamp'])
        self.data_frame['Browser_producer'] = self.data_frame['browser'].apply(get_browser_producer)
        self.data_frame['Status_type'] = self.data_frame['status'].apply(get_status_type)
        self.data_frame['Is_error'] = self.data_frame['Status_type']. apply(is_error)
        self.data_frame['hour'] = self.data_frame['timestamp'].apply(timestamp_to_hour)
        self.data_frame['minute'] = self.data_frame['timestamp'].apply(timestamp_to_minute)
        self.data_frame['browser_hour'] = self.data_frame['browser_timestamp'].apply(timestamp_to_hour)

    def _answer_first_question(self):
        active_users = self.data_frame['user_id']
        unique_users = count_distinct(active_users)
        print('ANSWER 1. There were', unique_users, 'unique users in the analysed period.')

    def _answer_second_question(self):
        users_per_hour = self.data_frame.pivot_table(values='user_id', index='hour', aggfunc=lambda x: len(x.unique()))
        users_per_hour = users_per_hour.to_dict()
        highest_activity = find_highest_value(users_per_hour)
        most_crowded_hour = highest_activity[0]
        most_crowded_hour_users_count = highest_activity[1]
        print('ANSWER 2. Most users were present at %s hours GMT-0 time. There were %s active users then.' % (
                                                                            most_crowded_hour,
                                                                            most_crowded_hour_users_count))

    def _answer_third_question(self):
        aux_pivot = self.data_frame.pivot_table(values=['timestamp', 'user_id', 'Is_error'],
                                                index='minute',
                                                aggfunc={'timestamp': 'count',
                                                         'user_id': lambda x: len(x.unique()),
                                                         'Is_error': 'sum'})

        aux_pivot['Error_rate'] = (aux_pivot['Is_error'] / aux_pivot['timestamp'])
        aux_pivot['Errors_per_active_user'] = (aux_pivot['Is_error'] / aux_pivot['user_id'])
        aux_dictionary = aux_pivot.to_dict()
        errors_per_user_per_minute = aux_dictionary['Errors_per_active_user']
        error_rate_per_minute = aux_dictionary['Error_rate']
        self._get_correlation_data(errors_per_user_per_minute)
        # self._get_correlation_data(error_rate_per_minute)

    def _get_correlation_data(self, correl_dict):
        correl_data = get_correl_data(correl_dict)
        correl_data = remove_outliers(correl_data)
        plotter.plot(correl_data[0], correl_data[1], 'o')
        polynomial = numpy.polyfit(correl_data[0], correl_data[1], 2)
        r_value = stats.linregress(correl_data[0], correl_data[1])[2]
        p_value = stats.linregress(correl_data[0], correl_data[1])[3]
        third_answer = self._get_third_answer(r_value, p_value, polynomial)
        print(third_answer)
        lower_limit = min(correl_data[0])
        upper_limit = max(correl_data[0])
        x = numpy.linspace(lower_limit, upper_limit, 1000)
        y = polynomial[0]*x**2 + x*polynomial[1] + polynomial[2]
        plotter.plot(x, y)
        plotter.show()

    def _get_third_answer(self, r_value, p_value, coefficients):
        if p_value < 0.05:
            return 'ANSWER 3. There is a significant non-linear correlation (p = %s) between time of the day and ' \
                   'crashes recorded. \n The equation for the correlation is %s*x^2 + %s*x + %s, and the R value is %s' \
                   % (p_value, coefficients[0], coefficients[1], coefficients[2], r_value)
        else:
            return 'There is no statisticaly significant non-linear correlation between time of the day and crashes' \
                   ' recorded.'