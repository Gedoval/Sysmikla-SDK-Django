from tests.integration.enviroment import clean_db


class TestEnviron:

    def test_clean_up_db(self):
        clean_db()

