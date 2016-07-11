from variables.variable_pattern import Variable

__author__ = 'michal-witkowski'

class AvgSessionTime(Variable):

    def __init__(self):
        Variable.__init__(self)
        self.variable_data = {}
        self.variable_name = 'AvgSessionTime'
        self.sessions_dict = {}

    def on_data_point(self, data_point):
        user_id = data_point[1]
        timestamp = int(data_point[2])
        if user_id not in self.variable_data:
            self.variable_data[user_id] = 0
            self.sessions_dict[user_id] = [[timestamp, timestamp]]
        else:
            self._update_sessions(user_id, timestamp)

    def _update_sessions(self, user_id, current_activity):
        half_hour_ms = 1800000
        last_activity = self.sessions_dict[user_id][-1][1]
        if current_activity - last_activity > half_hour_ms:
            self.sessions_dict[user_id].append([current_activity, current_activity])
        else:
            self.sessions_dict[user_id][-1][1] = current_activity

    def do_post_analysis(self):
        for user_id in self.sessions_dict:
            total_session_time = 0
            for session in self.sessions_dict[user_id]:
                session_time = session[1] - session[0]
                total_session_time += session_time
            session_count = len(self.sessions_dict[user_id])
            avg_session_time = total_session_time / session_count
            self.variable_data[user_id] = avg_session_time
