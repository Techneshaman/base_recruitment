from variables.variable_pattern import Variable

__author__ = 'michal-witkowski'

class FirstToLastActivity(Variable):

    def __init__(self):
        Variable.__init__(self)
        self.variable_data = {}
        self.variable_name = 'FirstToLastActivity'

    def on_data_point(self, data_point):
        user_id = data_point[1]
        timestamp = data_point[2]
        if user_id not in self.variable_data:
            self.variable_data[user_id] = [timestamp, timestamp]
        else:
            self.variable_data[user_id][1] = timestamp

    def do_post_analysis(self):
        for user_id in self.variable_data:
            first_active = self.variable_data[user_id][0]
            last_active = self.variable_data[user_id][1]
            self.variable_data[user_id] = int(last_active) - int(first_active)
