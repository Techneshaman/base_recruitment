from variables.variable_pattern import Variable

__author__ = 'michal-witkowski'

class StatusCount(Variable):

    def __init__(self, status_type='OK'):
        Variable.__init__(self)
        self.variable_data = {}
        self.variable_name = '%sStatusCount' % status_type
        self.status_type = status_type

    def on_data_point(self, data_point):
        user_id = data_point[1]
        status_number = data_point[5]
        status_type = self._get_status_type(status_number)
        if user_id not in self.variable_data:
            self.variable_data[user_id] = 0
        if status_type == self.status_type:
            self.variable_data[user_id] += 1

    def do_post_analysis(self):
        pass

    def _get_status_type(self, status_number):
        status_number = int(status_number)
        if status_number // 100 == 2:
            return 'OK'
        elif status_number // 100 == 4:
            return 'ClientError'
        elif status_number // 100 == 5:
            return 'ServerError'
        else:
            return 'Other'
