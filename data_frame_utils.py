__author__ = 'michal-witkowski'


def get_browser_producer(browser_version):
    browser_version = browser_version.split(' ')
    browser = browser_version[0]
    return browser


def timestamp_to_hour(timestamp):
    ms_in_day = 86400000
    ms_in_hour = 3600000
    hour = int((timestamp % ms_in_day - timestamp % ms_in_hour) / ms_in_hour)
    return hour


def timestamp_to_minute(timestamp):
    ms_in_day = 86400000
    ms_in_min = 60000
    quarter_in_a_day = (timestamp % ms_in_day - timestamp % ms_in_min) / ms_in_min
    return quarter_in_a_day


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


def count_distinct(data_series):
    distinct_values = set()
    for value in data_series:
        distinct_values.add(value)
    return len(distinct_values)


def find_highest_value(dictionary):
    highest_key = -1
    highest_value = 0
    for key in dictionary:
        value = dictionary[key]
        if value > highest_value:
            highest_key = key
            highest_value = value
    return [highest_key, highest_value]