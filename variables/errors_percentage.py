from variables.variable_pattern import Variable

__author__ = 'michal-witkowski'

class ErrorsPercentage(Variable):

    def __init__(self, error_type = 'total'):
        Variable.__init__(self)
        self.variable_data = {}
        self.variable_name = '%sErrorsPercentage' % error_type
        self.error_type = error_type

    def on_data_point(self, data_point):
        user_id = data_point[1]
        status_number = data_point[5]
        status_type = self._get_status_type(status_number)
        if user_id not in self.variable_data:
            self.variable_data[user_id] = [0, 0]
        self.variable_data[user_id][1] += 1
        if self.error_type == 'total' and status_type != 'OK':
            self.variable_data[user_id][0] += 1
        elif status_type == self.error_type:
            self.variable_data[user_id][0] += 1

    def do_post_analysis(self):
        for user_id in self.variable_data:
            errors = self.variable_data[user_id][0]
            all_requests = self.variable_data[user_id][1]
            errors_percentage = float(errors) / all_requests
            self.variable_data[user_id] = errors_percentage

    def _get_status_type(self, status_number):
        status_number = int(status_number)
        if status_number // 100 == 2:
            return 'OK'
        elif status_number // 100 == 4:
            return 'client'
        elif status_number // 100 == 5:
            return 'server'
        else:
            return 'other'