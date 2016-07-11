from variables.variable_pattern import Variable

__author__ = 'michal-witkowski'

class PlacesVisited(Variable):

    def __init__(self):
        Variable.__init__(self)
        self.variable_data = {}
        self.variable_name = 'PlacesVisited'
        self.places_list = ['sales', 'crm', 'email', 'settings', 'leads',
                            'tasks', 'reports', 'appointments', 'permissions']

    def on_data_point(self, data_point):
        user_id = data_point[1]
        if user_id not in self.variable_data:
            self.variable_data[user_id] = []
        place = data_point[8]
        place = place.lower()
        if place not in self.places_list:
            place = 'other'
        if place not in self.variable_data[user_id]:
            self.variable_data[user_id].append(place)

    def do_post_analysis(self):
        for user_id in self.variable_data:
            self.variable_data[user_id] = len(self.variable_data[user_id])
