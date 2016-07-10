import csv

__author__ = 'michal-witkowski'


class UsersAnalyser:

    def __init__(self, input_path):
        self.data = open(input_path, 'r')
        self.recoded_users = []
        self.variables_assignments = {}
        self.variables_list = []
        self.output_data = {}

    def register_variables(self, variables_list):
        self.variables_list = variables_list
        for variable in self.variables_list:
            variable.__init__(variable)

    def do_analysis(self):
        csv_reader = csv.reader(self.data)
        is_header = False
        for row in csv_reader:
            if not is_header:
                is_header = True
            else:
                self._analyse_row(row)
        self._do_post_analysis()

    def _analyse_row(self, row):
        user_id = row[1]
        if user_id not in self.output_data:
            self.output_data[user_id] = {}
        for variable in self.variables_list:
            variable.on_data_point(variable, row)

    def _do_post_analysis(self):
        for variable in self.variables_list:
            variable.do_post_analysis(variable)

    def get_output_data(self):
        output_header = []
        for variable in self.variables_list:
            variable_name = variable.__name__
            output_header.append(variable_name)
            for user_id in self.output_data:
                user_result = variable.variable_data[user_id]
                self.output_data[user_id][variable_name] = user_result
        print(output_header)
        for item in self.output_data:
            print(item, self.output_data[item])
