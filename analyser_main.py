__author__ = 'michal-witkowski'


from data_analyser import DataAnalyser

FILE_PATH = 'E:\\Workspace\\web_req_short.csv'
# FILE_PATH = 'E:\\Workspace\\web-requests-sample.csv'

if __name__ == '__main__':
    data_analyser = DataAnalyser(FILE_PATH)
    data_analyser.prepare_data()
    data_analyser.answer_the_questions()
    data_analyser.prepare_data_for_exploration()
