from data_frame_utils import *
from correlation_utils import *
import pandas
import numpy
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
        self._answer_extra_question()
        plotter.show()

    def export_enhanced_data(self, export_path):
        self.data_frame = self.data_frame.sort_values(by='timestamp')
        self.data_frame.to_csv(path_or_buf=export_path, index=False)

    def _cleanup_frame(self):
        self.data_frame.requestTime = pandas.to_numeric(self.data_frame.requestTime, errors='coerce')
        self.data_frame.pop('Unnamed: 0')

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
        unique_users_pivot = self.data_frame.pivot_table(index='user_id', values='hour', aggfunc='min')
        unique_users_per_hour = {}
        for item in unique_users_pivot:
            if item not in unique_users_per_hour:
                unique_users_per_hour[item] = 0
            unique_users_per_hour[item] += 1
        labels = []
        values = []
        for item in unique_users_per_hour:
            values.append(unique_users_per_hour[item])
            item = str(item) + ' hrs'
            labels.append(item)
        total = sum(values)
        colours = ['b', 'g', 'r', 'y', 'yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
        plotter.style.use('ggplot')
        plotter.pie(values, labels=labels, autopct=lambda p: '{:.0f}'.format(p * total / 100), colors=colours)
        plotter.title('ANSWER 1. (visualisation)\n Users per first hour of activity registered')
        print('ANSWER 1. There were', unique_users, 'unique users in the analysed period.')

    def _answer_second_question(self):
        users_per_hour = self.data_frame.pivot_table(values='user_id', index='hour', aggfunc=lambda x: len(x.unique()))
        self._plot_second_answer(users_per_hour)
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

    def _answer_extra_question(self):
        pivot_table = self.data_frame.pivot_table(index='account_id', values='user_id',
                                                  aggfunc=lambda x: len(x.unique()))
        users_per_account = {}
        total = 0
        for item in pivot_table:
            total += 1
            if item not in users_per_account:
                users_per_account[item] = 0
            users_per_account[item] += 1
        index = []
        values = []
        for item in users_per_account:
            index.append(item)
            values.append(users_per_account[item])
        plotter.figure()
        plotter.bar(index, values)
        multiaccounts = total - users_per_account[1]
        multiaccounts_percentage = (float(multiaccounts) * 100) / total
        print('EXTRA ANSWER. There are %s%% of accounts (N = %s) that are used by more than one user.'
              % (multiaccounts_percentage, multiaccounts))
        plotter.xlim([1, 5.9])
        plotter.title('EXTRA ANSWER (visualisation) \n Amount of unique users per account (xlim=5)')
        plotter.xlabel('Amount of unique users per single account')
        plotter.ylabel('Amount of accounts')


    def _get_correlation_data(self, correl_dict):
        correl_data = get_correl_data(correl_dict)
        correl_data = remove_outliers(correl_data)
        plotter.figure()
        plotter.title('ANSWER 3. (visualisation) \n Non-linear correlation between error rate and daytime.')
        plotter.ylabel('Errors per active users per minute')
        plotter.xlabel('Daytime (minutes of a day)')
        plotter.plot(correl_data[0], correl_data[1], 'o')
        polynomial = numpy.polyfit(correl_data[0], correl_data[1], 2)
        third_answer = self._get_third_answer(polynomial)
        print(third_answer)
        lower_limit = min(correl_data[0])
        upper_limit = max(correl_data[0])
        x_values = numpy.linspace(lower_limit, upper_limit, 1000)
        y_values = polynomial[0]*x_values**2 + x_values*polynomial[1] + polynomial[2]
        plotter.plot(x_values, y_values)

    def _get_third_answer(self, coefficients):
        return 'ANSWER 3. There is a non-linear correlation between time of the day and ' \
               'crashes recorded. \n The equation for the correlation is %s*x^2 + %s*x + %s.' \
               % (coefficients[0], coefficients[1], coefficients[2])

    def _plot_second_answer(self, users_per_hour):
        index = (users_per_hour.index.to_series()).tolist()
        values = users_per_hour.tolist()
        plotter.figure()
        plotter.bar(index, values)
        plotter.title('ANSWER 2. (visualisation)\n Active users per hour.')
        plotter.ylabel('Active users')
        plotter.xlabel('Daytime (hr)')
        plotter.xlim([0, 23])
