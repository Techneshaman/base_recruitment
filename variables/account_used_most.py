from variables.variable_pattern import Variable

__author__ = 'michal-witkowski'

class AccountUsedMost(Variable):

    def __init__(self):
        Variable.__init__(self)
        self.variable_data = {}
        self.variable_name = 'AccountUsedMost'

    def on_data_point(self, data_point):
        user_id = data_point[1]
        account_id = data_point[0]
        if user_id not in self.variable_data:
            self.variable_data[user_id] = {account_id: 0}
        elif account_id not in self.variable_data[user_id]:
            self.variable_data[user_id][account_id] = 0
        self.variable_data[user_id][account_id] += 1

    def do_post_analysis(self):
        for user_id in self.variable_data:
            max_requests = 0
            account_used_most = -1
            for account in self.variable_data[user_id]:
                uses_count = self.variable_data[user_id][account]
                if uses_count > max_requests:
                    account_used_most = account
                    max_requests = uses_count
            self.variable_data[user_id] = account_used_most
