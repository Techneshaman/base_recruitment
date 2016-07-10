from variables.variable_pattern import Variable

__author__ = 'michal-witkowski'

class RequestPlaceCount(Variable):

    def __init__(self, place='sales'):
        Variable.__init__(self)
        self.variable_data = {}
        self.variable_name = '%sRequestCount' % place
        self.place = place
        self.debug = []
        self.places_list = ['sales', 'crm', 'email', 'settings', 'leads',
                            'tasks', 'reports', 'appointments', 'permissions']

    def on_data_point(self, data_point):
        user_id = data_point[1]
        place = data_point[8]
        place = place.lower()
        if user_id not in self.variable_data:
            self.variable_data[user_id] = 0
        if place == self.place:
            self.variable_data[user_id] += 1
        elif self.place == 'other' and place not in self.places_list:
            self.variable_data[user_id] += 1

    def do_post_analysis(self):
        pass
