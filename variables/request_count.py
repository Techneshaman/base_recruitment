from variables.variable_pattern import Variable

__author__ = 'michal-witkowski'

class RequestCount(Variable):

    def __init__(self, request_type='get'):
        Variable.__init__(self)
        self.variable_data = {}
        self.variable_name = '%sRequestCount' % request_type
        self.request_type = request_type

    def on_data_point(self, data_point):
        user_id = data_point[1]
        if user_id not in self.variable_data:
            self.variable_data[user_id] = 0
        request_name = data_point[3]
        request_name = request_name.lower()
        if request_name == self.request_type:
            self.variable_data[user_id] += 1
