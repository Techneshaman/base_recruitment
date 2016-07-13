from variables.variable_pattern import Variable

__author__ = 'michal-witkowski'

class BrowserProducerUsed(Variable):

    def __init__(self, metric='count'):
        Variable.__init__(self)
        self.variable_data = {}
        self.variable_name = 'BrowserProducerUsed_%s' % metric
        self.metric = metric

    def on_data_point(self, data_point):
        user_id = data_point[1]
        if user_id not in self.variable_data:
            self.variable_data[user_id] = {}
        browser_used = data_point[6]
        browser_producer_used = browser_used.split(' ')[0]
        if browser_producer_used == 'Mozilla':
            browser_producer_used = 'Firefox'
        if browser_producer_used not in self.variable_data[user_id]:
            self.variable_data[user_id][browser_producer_used] = 0
        self.variable_data[user_id][browser_producer_used] += 1

    def do_post_analysis(self):
        if self.metric == 'count':
            for user_id in self.variable_data:
                browsers_used = 0
                for browser in self.variable_data[user_id]:
                    browsers_used += 1
                self.variable_data[user_id] = browsers_used
        elif self.metric == 'most':
            for user_id in self.variable_data:
                top_browser = ''
                max_requests = 0
                for browser in self.variable_data[user_id]:
                    requests_count = self.variable_data[user_id][browser]
                    if requests_count > max_requests:
                        top_browser = browser
                        max_requests = requests_count
                self.variable_data[user_id] = top_browser