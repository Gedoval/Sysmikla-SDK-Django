def convert_table_to_dict(table):
    return {f: v for f, v in table.rows}


class TestSession:
    def __init__(self, meli_id=None, access_token=None):
        self.meli_id = meli_id
        self.access_token = access_token

    def __repr__(self):
        return 'NotImplemented Lol'


class Constants:
    USER_QUERY_FIELDS = [
        'meli_id',
        'app_id',
        'app_secret',
        'redirect_url'
    ]

