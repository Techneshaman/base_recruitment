from variables.variable_pattern import Variable

__author__ = 'michal-witkowski'

class TopNFeaturePercentage(Variable):

    def __init__(self, n=1):
        Variable.__init__(self)
        self.variable_data = {}
        self.variable_name = 'Top%sFeaturePercentage' % n
        self.n = n
        self.places_list = ['sales', 'crm', 'email', 'settings', 'leads',
                            'tasks', 'reports', 'appointments', 'permissions']

    def on_data_point(self, data_point):
        user_id = data_point[1]
        if user_id not in self.variable_data:
            self.variable_data[user_id] = {}
        place = data_point[8]
        place = place.lower()
        if place not in self.places_list:
            place = 'other'
        if place not in self.variable_data[user_id]:
            self.variable_data[user_id][place] = 0
        self.variable_data[user_id][place] += 1

    def do_post_analysis(self):
        for user_id in self.variable_data:
            features_used = []
            requests_count = 0
            for place in self.variable_data[user_id]:
                count = self.variable_data[user_id][place]
                requests_count += count
                visits_list = [count, place]
                features_used.append(visits_list)
            index = 0
            for item in features_used:
                features_used[index][0] = float(item[0]) / requests_count
                features_used[index] = tuple(features_used[index])
                index += 1
            features_used.sort(key=lambda tup: tup[0], reverse=True)
            if self.n > len(features_used):
                self.variable_data[user_id] = 'NA'
            else:
                index = self.n - 1
                top_n_feature_percentage = features_used[index][0]
                self.variable_data[user_id] = top_n_feature_percentage
