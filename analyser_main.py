import pandas
import numpy
import matplotlib.pyplot

# path = 'E:\\Workspace\\web_req_short.csv'
path = 'E:\\Workspace\\web-requests-sample.csv'
data_frame = pandas.read_csv(path, sep=',')
# data_frame = data_frame.drop(data_frame.columns[[0]], axis=1)
# data_frame.request = data_frame.request.replace(to_replace='GET', value=numpy.nan)
data_frame.requestTime = pandas.to_numeric(data_frame.requestTime, errors='coerce')
print(data_frame.describe())

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

data_frame['timestampDiff'] = data_frame['browser_timestamp'].sub(data_frame['timestamp'])
data_frame['Browser_producer'] = data_frame['browser'].apply(get_browser_producer)
data_frame['Status_type'] = data_frame['status'].apply(get_status_type)

data_frame['timestamp'] = data_frame['timestamp'].apply(timestamp_to_hour)
data_frame['browser_timestamp'] = data_frame['browser_timestamp'].apply(timestamp_to_hour)
data_frame.rename(columns={'timestamp': 'hour', 'browser_timestamp': 'browser_hour'}, inplace=True)
print(data_frame)
# print(data_frame.dtypes)
# print(data_frame.describe())

user_pivot = data_frame.pivot_table(values='user_id', index='status', columns='Status_type', aggfunc='count')
print(user_pivot)
print(user_pivot.describe())
