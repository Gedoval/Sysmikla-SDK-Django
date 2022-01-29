from rest_framework.exceptions import APIException

class BadTokenException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'[ERROR] {self.message}'


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'

class NoSuchUserException(APIException):
    status_code = 401
    default_detail = 'No user found for ID:'
    default_code = 'no_such_user'

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f'{self.default_detail} {self.user_id}'

