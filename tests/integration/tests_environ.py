from tests.integration.enviroment import clean_db
from tests.integration.steps.steps_auth import *
import behave.runner
from apps.mercadolibre.models import User
from rest_framework.test import APITestCase


class TestEnviron(APITestCase):
    user_info = {
        'HTTP_TG_CODE': 'TG-1234',
        'HTTP_REDIRECT_URL': 'https://sfsdfs.com',
        'HTTP_APP_ID': 'A23242',
        'HTTP_APP_SECRET': 'SADADADSA',
        'HTTP_MELI_ID': '52073370',
        'ACCESS_TOKEN': 'AG-123456',
        'REFRESH_TOKEN': 'TG-987654321'
    }

    def test_clean_up_db(self):
        clean_db()

    def test_select_user_sql(self):
        self.__create_mock_user()
        context = behave.runner.Context(behave.runner.Runner(None))
        context.session = TestSession(meli_id=TestEnviron.user_info['HTTP_MELI_ID'])
        check_for_user_update(context)

    def __create_mock_user(self):
        user = User(
            app_id=TestEnviron.user_info['HTTP_APP_ID'],
            app_secret=TestEnviron.user_info['HTTP_APP_SECRET'],
            meli_id=TestEnviron.user_info['HTTP_MELI_ID'],
            access_token=TestEnviron.user_info['ACCESS_TOKEN'],
            refresh_token=TestEnviron.user_info['REFRESH_TOKEN']
        )
        user.save()

