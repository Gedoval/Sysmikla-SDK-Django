class BadTokenException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'[ERROR] {self.message}'
