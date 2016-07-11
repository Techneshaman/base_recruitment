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
        print('Initialising variables...')
        self.variables_list = variables_list

    def do_analysis(self):
        csv_reader = csv.reader(self.data)
        is_header = False
        print('Starting analysis...')
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
            variable.on_data_point(row)

    def _do_post_analysis(self):
        print('Starting post-analysis...')
        for variable in self.variables_list:
            variable.do_post_analysis()

    def get_output_data(self, output_path):
        output_header = []
        for variable in self.variables_list:
            variable_name = variable.variable_name
            output_header.append(variable_name)
            for user_id in self.output_data:
                user_result = variable.variable_data[user_id]
                self.output_data[user_id][variable_name] = user_result
        output_file = open(output_path, 'w')
        csv_writer = csv.writer(output_file, lineterminator='\n')
        header_row = ['UserID'] + output_header
        csv_writer.writerow(header_row)
        print('Writing output file...')
        for user_id in self.output_data:
            row = [str(user_id)]
            for item in output_header:
                row.append(str(self.output_data[user_id][item]))
            csv_writer.writerow(row)
        output_file.close()
