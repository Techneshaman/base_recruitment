import numpy

__author__ = 'michal-witkowski'


def get_correl_data(dictionary):
    variable_a = []
    variable_b = []
    for key in dictionary:
        value = dictionary[key]
        variable_a.append(key)
        variable_b.append(value)
    return variable_a, variable_b


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


def normalise(correl_data):
    for variable in correl_data:
        mean = numpy.mean(variable)
        stdev = numpy.std(variable)
        index = 0
        for item in variable:
            new_item = (item - mean) / stdev
            variable[index] = new_item
            index += 1
    return correl_data
