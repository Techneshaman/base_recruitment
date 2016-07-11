from variables.variable_pattern import Variable
import numpy

__author__ = 'michal-witkowski'

class LastNRequestErrors(Variable):

    def __init__(self, n=1):
        Variable.__init__(self)
        self.variable_data = {}
        self.variable_name = 'Last%sRequestErrors' % n
        self.n = n

    def on_data_point(self, data_point):
        user_id = data_point[1]
        if user_id not in self.variable_data:
            self.variable_data[user_id] = []
        is_error = int(data_point[12])
        self._update_requests_time(user_id, is_error)

    def do_post_analysis(self):
        for user_id in self.variable_data:
            self.variable_data[user_id] = sum(self.variable_data[user_id])

    def _update_requests_time(self, user_id, request_time):
        if len(self.variable_data[user_id]) < self.n:
            self.variable_data[user_id].append(request_time)
        else:
            del self.variable_data[user_id][0]
            self.variable_data[user_id].append(request_time)

