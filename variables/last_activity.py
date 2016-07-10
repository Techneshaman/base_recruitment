from variables.variable_pattern import Variable

__author__ = 'michal-witkowski'

class LastActivity(Variable):

    def __init__(self):
        Variable.__init__(self)
        self.variable_data = {}

    def on_data_point(self, data_point):
        user_id = data_point[1]
        timestamp = data_point[2]
        self.variable_data[user_id] = timestamp

    def do_post_analysis(self):
        pass
        # print("LAST ACTIVITY")
        # for user in self.variable_data:
        #     print(user, self.variable_data[user])