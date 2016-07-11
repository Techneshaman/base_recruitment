from variables.variable_pattern import Variable
import numpy

__author__ = 'michal-witkowski'

class AvgBrowserServerTimeDiff(Variable):

    def __init__(self):
        Variable.__init__(self)
        self.variable_data = {}
        self.variable_name = 'AvgBrowserServerTimeDiff'

    def on_data_point(self, data_point):
        user_id = data_point[1]
        time_diff = int(data_point[9])
        if user_id not in self.variable_data:
            self.variable_data[user_id] = []
        self.variable_data[user_id].append(time_diff)

    def do_post_analysis(self):
        for user_id in self.variable_data:
            self.variable_data[user_id] = numpy.average(self.variable_data[user_id])
