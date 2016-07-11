from variables.variable_pattern import Variable
from numpy import average

__author__ = 'michal-witkowski'

class AvgRequestTime(Variable):

    def __init__(self):
        Variable.__init__(self)
        self.variable_data = {}
        self.variable_name = 'AvgRequestTime'

    def on_data_point(self, data_point):
        user_id = data_point[1]
        request_time = data_point[4]
        if user_id not in self.variable_data:
            self.variable_data[user_id] = []
        try:
            request_time = float(request_time)
            self.variable_data[user_id].append(request_time)
        except:
            pass

    def do_post_analysis(self):
        for user_id in self.variable_data:
            if len(self.variable_data[user_id]) < 1:
                self.variable_data[user_id] = -1
            else:
                avg_time = int(average(self.variable_data[user_id]))
                self.variable_data[user_id] = avg_time
