from variables.variable_pattern import Variable

__author__ = 'michal-witkowski'

class PlaceUsedMost(Variable):

    def __init__(self):
        Variable.__init__(self)
        self.variable_data = {}
        self.variable_name = 'PlaceUsedMost'
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
            max_requests = 0
            top_visited = ''
            for place in self.variable_data[user_id]:
                requests_count = self.variable_data[user_id][place]
                if requests_count > max_requests:
                    max_requests = requests_count
                    top_visited = place
            self.variable_data[user_id] = top_visited
