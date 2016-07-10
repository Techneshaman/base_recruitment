__author__ = 'michal-witkowski'


from data_analyser import DataAnalyser
from users_analyser import UsersAnalyser
from variables.first_activity import FirstActivity
from variables.last_activity import LastActivity

SOURCE_FILE_PATH = 'E:\\Workspace\\web_req_short.csv'
# SOURCE_FILE_PATH = 'E:\\Workspace\\web-requests-sample.csv'
ENHANCED_FILE_PATH = 'E:\\Workspace\\web_req_enhanced.csv'

variables_list = [FirstActivity,
                  LastActivity]

if __name__ == '__main__':
    # data_analyser = DataAnalyser(SOURCE_FILE_PATH)
    # data_analyser.prepare_data()
    # data_analyser.answer_the_questions()
    # data_analyser.export_enhanced_data(ENHANCED_FILE_PATH)

    users_analyser = UsersAnalyser(ENHANCED_FILE_PATH)
    users_analyser.register_variables(variables_list)
    users_analyser.do_analysis()
    users_analyser.get_output_data()
