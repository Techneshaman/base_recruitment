__author__ = 'michal-witkowski'

import pandas
import numpy
import matplotlib.pyplot as plotter

# path = 'E:\\Workspace\\web_req_short.csv'
path = 'E:\\Workspace\\web-requests-sample.csv'
data_frame = pandas.read_csv(path, sep=',')
# data_frame = data_frame.drop(data_frame.columns[[0]], axis=1)
# data_frame.request = data_frame.request.replace(to_replace='GET', value=numpy.nan)
data_frame.requestTime = pandas.to_numeric(data_frame.requestTime, errors='coerce')
# print(data_frame.describe())


def timestamp_to_hour(timestamp):
    ms_in_day = 86400000
    ms_in_hour = 3600000
    hour = int((timestamp % ms_in_day - timestamp % ms_in_hour) / ms_in_hour)
    return hour


def get_browser_producer(browser_version):
    browser_version = browser_version.split(' ')
    browser = browser_version[0]
    return browser


def get_status_type(status_number):
    status_number = int(status_number)
    if status_number // 100 == 2:
        return 'OK'
    elif status_number // 100 == 4:
        return 'ClientError'
    elif status_number // 100 == 5:
        return 'ServerError'
    else:
        return 'Other'


def is_error(status_type):
    if status_type == 'OK':
        return 0
    else:
        return 1


def find_highest_value(dictionary):
    highest_key = -1
    highest_value = 0
    for key in dictionary:
        value = dictionary[key]
        if value > highest_value:
            highest_key = key
            highest_value = value
    return [highest_key, highest_value]


def count_distinct(data_series):
    distinct_values = set()
    for value in data_series:
        distinct_values.add(value)
    return len(distinct_values)


def timestamp_to_minute(timestamp):
    ms_in_day = 86400000
    ms_in_min = 60000
    quarter_in_a_day = (timestamp % ms_in_day - timestamp % ms_in_min) / ms_in_min
    return quarter_in_a_day


data_frame['timestampDiff'] = data_frame['browser_timestamp'].sub(data_frame['timestamp'])
data_frame['Browser_producer'] = data_frame['browser'].apply(get_browser_producer)
data_frame['Status_type'] = data_frame['status'].apply(get_status_type)
data_frame['Is_error'] = data_frame['Status_type']. apply(is_error)

data_frame['hour'] = data_frame['timestamp'].apply(timestamp_to_hour)
data_frame['minute'] = data_frame['timestamp'].apply(timestamp_to_minute)
data_frame['browser_hour'] = data_frame['browser_timestamp'].apply(timestamp_to_hour)
# data_frame.rename(columns={'timestamp': 'hour', 'browser_timestamp': 'browser_hour'}, inplace=True)
# print(data_frame)
# print(data_frame.dtypes)
# print(data_frame.describe())

active_users = data_frame['user_id']
unique_users = count_distinct(active_users)
print('ANSWER 1. There were', unique_users, 'unique users in the analysed period.')

users_per_hour = data_frame.pivot_table(values='user_id', index='hour', aggfunc=lambda x: len(x.unique()))
# print(users_per_hour)
# print(users_per_hour.describe())
users_per_hour = users_per_hour.to_dict()
highest_activity = find_highest_value(users_per_hour)
most_crowded_hour = highest_activity[0]
most_crowded_hour_users_count = highest_activity[1]
print('ANSWER 2. Most users were present at %s hours GMT-0 time. There were %s active users then.' % (most_crowded_hour,
                                                                                most_crowded_hour_users_count))

aux_pivot = data_frame.pivot_table(values=['timestamp', 'user_id', 'Is_error'],
                                   index='minute',
                                   aggfunc={'timestamp': 'count',
                                            'user_id': lambda x: len(x.unique()),
                                            'Is_error': 'sum'})

aux_pivot['Error_rate'] = aux_pivot['Is_error'] / aux_pivot['timestamp']
aux_pivot2 = aux_pivot.to_dict()
correl_dict = aux_pivot2['Error_rate']


def get_correl_data(dictionary):
    variable_a = []
    variable_b = []
    for key in dictionary:
        value = dictionary[key]
        variable_a.append(key)
        variable_b.append(value)
    return variable_a, variable_b

correl_data = get_correl_data(correl_dict)

def remove_outliers(correl_data):
    variable_a = correl_data[0]
    outliers_values_a = find_outliers_values(variable_a)
    variable_b = correl_data[1]
    outliers_values_b = find_outliers_values(variable_b)
    tuples_array = list(zip(variable_a, variable_b))
    index = 0
    indexes_to_remove = []
    for item in tuples_array:
        if is_outlying_value(item, outliers_values_a, outliers_values_b):
            indexes_to_remove.append(index)
        index += 1
    variable_a = remove_values_by_index(variable_a, indexes_to_remove)
    variable_b = remove_values_by_index(variable_b, indexes_to_remove)
    return variable_a, variable_b


def find_outliers_values(list):
    deviation = numpy.std(list)
    mean = numpy.mean(list)
    outlier_low = mean - 3 * deviation
    outlier_high = mean + 3 * deviation
    return outlier_low, outlier_high

def is_outlying_value(tuple, outliers_a, outliers_b):
    value_a = tuple[0]
    value_b = tuple[1]
    if value_a < outliers_a[0] or value_a > outliers_a[1]:
        return True
    elif value_b < outliers_b[0] or value_b > outliers_b[1]:
        return True
    else:
        return False

def remove_values_by_index(old_list, indexes_to_remove):
    index = 0
    new_list = []
    for item in old_list:
        if index not in indexes_to_remove:
            new_list.append(item)
        index += 1
    return new_list

correl_data = remove_outliers(correl_data)
plotter.plot(correl_data[0], correl_data[1], 'o')
plotter.show()
