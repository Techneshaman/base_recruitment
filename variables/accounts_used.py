from variables.variable_pattern import Variable

__author__ = 'michal-witkowski'

class AccountsUsed(Variable):

    def __init__(self):
        Variable.__init__(self)
        self.variable_data = {}
        self.variable_name = 'AccountsUsed'

    def on_data_point(self, data_point):
        user_id = data_point[1]
        account_id = data_point[0]
        if user_id not in self.variable_data:
            self.variable_data[user_id] = [account_id]
        elif account_id not in self.variable_data[user_id]:
            self.variable_data[user_id].append(account_id)

    def do_post_analysis(self):
        for user_id in self.variable_data:
            self.variable_data[user_id] = len(self.variable_data[user_id])
