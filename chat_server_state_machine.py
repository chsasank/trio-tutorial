class Event:
    NEW_CONNECTION = 'NEW_CONNECTION'
    VALID_USER_NAME = 'VALID_USER_NAME'
    INVALID_USER_NAME = 'INVALID_USER_NAME'
    MESSAGE = 'MESSAGE'
    CLOSE_CONNECTION = 'CLOSE_CONNECTION'

    def __init__(self, event_type, data=None):
        self.event_type = event_type
        self.data = data


class StateMachine:
    IDLE = 'IDLE'
    USER_LOGIN = 'USER_LOGIN'
    USER_LOGGED_IN = 'USER_LOGGED_IN'
    DONE = 'DONE'

    TRANSITIONS = {
        IDLE: {
            Event.NEW_CONNECTION: USER_LOGIN,
            Event.CLOSE_CONNECTION: DONE
        },
        USER_LOGIN: {
            Event.VALID_USER_NAME: USER_LOGGED_IN,
            Event.INVALID_USER_NAME: USER_LOGIN,
            Event.CLOSE_CONNECTION: DONE
        },
        USER_LOGGED_IN: {
            Event.MESSAGE: USER_LOGGED_IN,
            Event.CLOSE_CONNECTION: DONE
        }
    }

    def __init__(self):
        self._state = self.IDLE
    
    def _transition(self, event):
        self._state = TRANSITIONS[self._state][event.event_type]


class ChatServerSansIO:
    def __init__(self):
        # place to store list of current users
        # this is why we used a class instead of a function
        self.connections = {}

    def receive_data(self, connection, data):

    def server(self, server_stream):


if __name__ == '__main__':
    StateMachine()

