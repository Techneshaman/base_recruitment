__author__ = 'michal-witkowski'

class Variable:

    def __init__(self):
        self.variable_data = {}
        self.variable_name = 'NA'

    def on_data_point(self, data_point):
        pass

    def do_post_analysis(self):
        pass
