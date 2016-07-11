__author__ = 'michal-witkowski'


from data_analyser import DataAnalyser
from users_analyser import UsersAnalyser
from variables.first_activity import FirstActivity
from variables.last_activity import LastActivity
from variables.request_count import RequestCount
from variables.browser_used import BrowserUsed
from variables.status_count import StatusCount
from variables.request_place_count import RequestPlaceCount
from variables.avg_request_time import AvgRequestTime
from variables.incorrect_request_time import IncorrectRequestTime
from variables.session_counter import SessionCounter
from variables.avg_session_time import AvgSessionTime
from variables.accounts_used import AccountsUsed
from variables.account_used_most import AccountUsedMost
from variables.avg_browser_server_time_diff import AvgBrowserServerTimeDiff
from variables.last_n_requests_time import AvgLastNRequestsTime
from variables.last_n_request_errors import LastNRequestErrors
from variables.places_visited import PlacesVisited
from variables.place_used_most import PlaceUsedMost

# SOURCE_FILE_PATH = 'E:\\Workspace\\web_req_short.csv'
SOURCE_FILE_PATH = 'E:\\Workspace\\web-requests-sample.csv'
ENHANCED_FILE_PATH = 'E:\\Workspace\\web_req_enhanced.csv'
USER_CENTRED_DATA_PATH = 'E:\\Workspace\\web_req_per_player.csv'

variables_list = [
                  FirstActivity(),
                  SessionCounter(),
                  AvgSessionTime(),
                  AccountsUsed(),
                  AccountUsedMost(),
                  AvgBrowserServerTimeDiff(),
                  AvgLastNRequestsTime(n=10),
                  LastNRequestErrors(n=10),
                  LastNRequestErrors(n=1),
                  LastActivity(),
                  RequestCount('get'),
                  RequestCount('post'),
                  RequestCount('put'),
                  RequestCount('delete'),
                  BrowserUsed('count'),
                  BrowserUsed('most'),
                  StatusCount('OK'),
                  StatusCount('ServerError'),
                  StatusCount('ClientError'),
                  StatusCount('Other'),
                  PlacesVisited(),
                  PlaceUsedMost(),
                  RequestPlaceCount('sales'),
                  RequestPlaceCount('crm'),
                  RequestPlaceCount('email'),
                  RequestPlaceCount('settings'),
                  RequestPlaceCount('leads'),
                  RequestPlaceCount('tasks'),
                  RequestPlaceCount('reports'),
                  RequestPlaceCount('appointments'),
                  RequestPlaceCount('permissions'),
                  RequestPlaceCount('other'),
                  AvgRequestTime(),
                  IncorrectRequestTime()
                  ]

if __name__ == '__main__':
    data_analyser = DataAnalyser(SOURCE_FILE_PATH)
    data_analyser.prepare_data()
    data_analyser.answer_the_questions()
    data_analyser.export_enhanced_data(ENHANCED_FILE_PATH)

    users_analyser = UsersAnalyser(ENHANCED_FILE_PATH)
    users_analyser.register_variables(variables_list)
    users_analyser.do_analysis()
    users_analyser.get_output_data(USER_CENTRED_DATA_PATH)
    print('Analysis complete.')
