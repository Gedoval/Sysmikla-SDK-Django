import json
from pathlib import Path
from rest_framework.test import APITestCase, RequestsClient
from django.urls import reverse
import requests_mock
from hamcrest import *
from rest_framework import status
from apps.mercadolibre.tasks import store_token_and_user
from apps.mercadolibre.models import User
from apps.redis.handler import RedisHandler
from apps.mercadolibre.constants import Constants as CONST

redis = RedisHandler()


class MercadoLibreTest(APITestCase):
    user_info = {
        'HTTP_TG_CODE': 'TG-1234',
        'HTTP_REDIRECT_URL': 'https://sfsdfs.com',
        'HTTP_APP_ID': 'A23242',
        'HTTP_APP_SECRET': 'SADADADSA',
        'HTTP_MELI_ID': '52073370'
    }
    BASE_DIR = Path(__file__).resolve().parent.parent

    def test_get_token(self):
        with requests_mock.Mocker() as m:
            url = reverse('get-token')
            m.post(
                url=CONST.API_HOST + CONST.TOKEN_URL,
                json=json.load(open(str(MercadoLibreTest.BASE_DIR) + "/tests/resources/mock_token.json"))
            )

            response = self.client.get(
                url,
                **{
                    'HTTP_TG_CODE': 'TG-1234',
                    'HTTP_REDIRECT_URL': 'https://sfsdfs.com',
                    'HTTP_APP_ID': 'A23242',
                    'HTTP_APP_SECRET': 'SADADADSA'
                }
            )
            assert_that(response.status_code, status.HTTP_200_OK)
            assert_that(response.data,
                        json.load(open(str(MercadoLibreTest.BASE_DIR) + "/tests/resources/mock_token.json")))

    def test_missing_headers(self):
        with requests_mock.Mocker() as m:
            url = reverse('get-token')
            m.post(
                url=CONST.API_HOST + CONST.TOKEN_URL,
                json=json.load(open(str(MercadoLibreTest.BASE_DIR) + "/tests/resources/mock_token.json"))
            )
            response = self.client.get(
                url
            )
            assert_that(response, not_none())
            assert_that(response.json(), equal_to('Missing required headers'))

    def test_bad_token_response(self):
        with requests_mock.Mocker() as m:
            url = reverse('get-token')
            m.post(
                url=CONST.API_HOST + CONST.TOKEN_URL,
                json=json.load(open(str(MercadoLibreTest.BASE_DIR) + '/tests/resources/mock_bad_response.json'))
            )
            response = self.client.get(
                url,
                **{
                    'HTTP_TG_CODE': 'TG-1234',
                    'HTTP_REDIRECT_URL': 'https://sfsdfs.com',
                    'HTTP_APP_ID': 'A23242',
                    'HTTP_APP_SECRET': 'SADADADSA'
                }
            )
            assert_that(response, not_none())
            assert_that(response.json(), has_key('error'))

    def test_unavailable_service(self):
        with requests_mock.Mocker() as m:
            url = reverse('get-token')
            m.post(
                url='http://jejojejo' + CONST.TOKEN_URL,
                json=json.load(open(str(MercadoLibreTest.BASE_DIR) + '/tests/resources/mock_bad_response.json'))
            )
            response = self.client.get(
                url,
                **{
                    'HTTP_TG_CODE': 'TG-1234',
                    'HTTP_REDIRECT_URL': 'https://sfsdfs.com',
                    'HTTP_APP_ID': 'A23242',
                    'HTTP_APP_SECRET': 'SADADADSA'
                }
            )
            assert_that(response.json(), has_value('Service temporarily unavailable, try again later.'))

    def test_task_store_user_and_token(self):
        token = json.load(open(str(MercadoLibreTest.BASE_DIR) + "/tests/resources/mock_token.json"))
        store_token_and_user(
            token,
            MercadoLibreTest.user_info['HTTP_APP_ID'],
            MercadoLibreTest.user_info['HTTP_APP_SECRET'],
            MercadoLibreTest.user_info['HTTP_REDIRECT_URL']
        )
        meli_id = token['user_id']
        query_set = User.objects.all()
        assert_that(query_set, has_length(1))
        obj = redis.get(f'user:{meli_id}')
        assert_that(obj, json.dumps(token))

    def test_task_update_user_token(self):
        self.__create_mock_user()
        query_set = User.objects.all()
        assert_that(query_set, has_length(1))
        meli_id = MercadoLibreTest.user_info['HTTP_MELI_ID']
        token = json.load(open(str(MercadoLibreTest.BASE_DIR) + "/tests/resources/mock_token.json"))
        token.update({'access_token': 'BOGUS'})
        redis.setex(
            f'user:{meli_id}',
            value=token
        )
        token = json.load(open(str(MercadoLibreTest.BASE_DIR) + "/tests/resources/mock_token.json"))
        store_token_and_user(
            token,
            MercadoLibreTest.user_info['HTTP_APP_ID'],
            MercadoLibreTest.user_info['HTTP_APP_SECRET'],
            MercadoLibreTest.user_info['HTTP_REDIRECT_URL']
        )
        query_set = User.objects.all()
        assert_that(query_set, has_length(1))
        redis_token = redis.get(f'user:{meli_id}')
        assert_that(redis_token.get('access_token'), is_not('BOGUS'))
        assert_that(redis_token, json.dumps(token))

    def test_task_user_create_exception(self):
        token = json.load(open(str(MercadoLibreTest.BASE_DIR) + "/tests/resources/mock_token.json"))
        store_token_and_user(
            token,
            list(),
            list(),
            dict()
        )
        error = redis.get('user_error:' + str(token['user_id']))
        assert_that(error, not_none(), 'We should have an error for the current user on redis')
        query_set = User.objects.all()
        assert_that(query_set, has_length(0))

    def test_get_categories(self):
        with requests_mock.Mocker() as m:
            url = reverse('get-category', kwargs={'category_id': '123456'})
            response_body = json.load(open(str(MercadoLibreTest.BASE_DIR) + '/tests/resources/mock_category.json'))
            m.get(
                url=CONST.API_HOST + CONST.CATEGORIES + '/123456',
                json=response_body
            )
            response = self.client.get(
                url
            )
            assert_that(response.status_code, equal_to(200))
            assert_that(response.data, equal_to(response_body))

    def test_get_categories_attributes(self):
        with requests_mock.Mocker() as m:
            url = reverse('get-category-attributes', kwargs={'category_id': '123456'})
            response_body = json.load(
                open(str(MercadoLibreTest.BASE_DIR) + '/tests/resources/mock_category_attributes.json'))
            m.get(
                url=CONST.API_HOST + CONST.CATEGORIES + '/123456/attributes',
                json=response_body
            )
            response = self.client.get(
                url
            )
            assert_that(response.status_code, equal_to(200))
            assert_that(response.data, equal_to(response_body))

    def test_successfully_publish_realstate(self):
        with requests_mock.Mocker() as m:
            url = reverse('realstate-insert')
            m.post(
                url=CONST.API_HOST + CONST.ITEMS,
                json=json.load(open(str(MercadoLibreTest.BASE_DIR) + '/tests/resources/mock_realstate_response.json'))
            )
            mock_token = json.load(open(str(MercadoLibreTest.BASE_DIR) + '/tests/resources/mock_token.json'))
            redis.setex('MLA123456', mock_token)
            body = json.load(open(str(MercadoLibreTest.BASE_DIR) + '/tests/resources/mock_sync_event_realstate.json'))
            response = self.client.post(
                url,
                json.dumps(body),
                format='json',
                **{'HTTP_USER_ID': 'MLA123456'}
            )
            assert_that(response.status_code, same_instance(200))
            assert_that(redis.is_in_set(CONST.USER_LOCK, 'MLA123456'), equal_to(False), 'User is still locked')
            redis.clear_set(CONST.USER_LOCK)

    def test_successfully_publish_realstate_with_no_user_on_redis(self):
        with requests_mock.Mocker() as m:
            url = reverse('realstate-insert')
            response_body = json.load(
                open(str(MercadoLibreTest.BASE_DIR) + '/tests/resources/mock_realstate_response.json'))
            m.post(
                url=CONST.API_HOST + CONST.ITEMS,
                json=response_body
            )
            self.__create_mock_user()
            body = json.load(open(str(MercadoLibreTest.BASE_DIR) + '/tests/resources/mock_sync_event_realstate.json'))
            response = self.client.post(
                url,
                json.dumps(body),
                format='json',
                **{'HTTP_USER_ID': MercadoLibreTest.user_info['HTTP_MELI_ID']}
            )
            assert_that(response.status_code, same_instance(200))
            assert_that(response.data, equal_to(response_body))
            assert_that(redis.is_in_set(CONST.USER_LOCK, MercadoLibreTest.user_info['HTTP_MELI_ID']), equal_to(False),
                        'User is still locked')
            redis.clear_set(CONST.USER_LOCK)

    def test_unsuccessfull_realstate_post(self):
        with requests_mock.Mocker() as m:
            url = reverse('realstate-insert')
            response_body = json.load(
                open(str(MercadoLibreTest.BASE_DIR) + '/tests/resources/mock_realstate_response.json'))
            m.post(
                url=CONST.API_HOST + CONST.ITEMS,
                json=response_body
            )
            body = json.load(open(str(MercadoLibreTest.BASE_DIR) + '/tests/resources/mock_sync_event_realstate.json'))
            response = self.client.post(
                url,
                json.dumps(body),
                format='json',
                **{'HTTP_USER_ID': MercadoLibreTest.user_info['HTTP_MELI_ID']}
            )
            assert_that(response.status_code, equal_to(401))
            assert_that(response.data, has_string('No user found for ID: 52073370'))

    def __create_mock_user(self):
        user = User(
            app_id=MercadoLibreTest.user_info['HTTP_APP_ID'],
            app_secret=MercadoLibreTest.user_info['HTTP_APP_SECRET'],
            meli_id=MercadoLibreTest.user_info['HTTP_MELI_ID']
        )
        user.save()
