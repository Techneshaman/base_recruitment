from variables.variable_pattern import Variable

__author__ = 'michal-witkowski'

class IncorrectRequestTime(Variable):

    def __init__(self):
        Variable.__init__(self)
        self.variable_data = {}
        self.variable_name = 'IncorrectRequestTime'

    def on_data_point(self, data_point):
        user_id = data_point[1]
        request_time = data_point[4]
        if user_id not in self.variable_data:
            self.variable_data[user_id] = 0
        try:
            request_time = float(request_time)
        except:
            self.variable_data[user_id] += 1
