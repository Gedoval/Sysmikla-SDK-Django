import json
from pathlib import Path
from rest_framework.test import APITestCase
from django.urls import reverse
from apps.mercadolibre.constants import Constants as Consts
import requests_mock
from hamcrest import *
from rest_framework import status
from apps.mercadolibre.tasks import store_token_and_user
from apps.mercadolibre.models import User
from tests.settings import r as redis


class TokenTest(APITestCase):
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
                url=Consts.API_HOST + Consts.TOKEN_URL,
                json=json.load(open(str(TokenTest.BASE_DIR) + "/tests/resources/mock_token.json"))
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
            assert_that(response.data, json.load(open(str(TokenTest.BASE_DIR) + "/tests/resources/mock_token.json")))

    def test_store_user_and_token(self):
        token = json.load(open(str(TokenTest.BASE_DIR) + "/tests/resources/mock_token.json"))
        store_token_and_user(
            token,
            TokenTest.user_info['HTTP_APP_ID'],
            TokenTest.user_info['HTTP_APP_SECRET'],
            TokenTest.user_info['HTTP_REDIRECT_URL']
        )
        meli_id = token['user_id']
        query_set = User.objects.all()
        assert_that(len(query_set), 1)
        obj = redis.get(f'user:{meli_id}')
        assert_that(json.loads(obj), json.dumps(token))

    def test_update_user_token(self):
        self.__create_mock_user()
        query_set = User.objects.all()
        assert_that(len(query_set), 1)
        meli_id = TokenTest.user_info['HTTP_MELI_ID']
        token = json.load(open(str(TokenTest.BASE_DIR) + "/tests/resources/mock_token.json"))
        token.update({'access_token': 'BOGUS'})
        redis.set(
            f'user:{meli_id}',
            value=json.dumps(token)
        )
        token = json.load(open(str(TokenTest.BASE_DIR) + "/tests/resources/mock_token.json"))
        store_token_and_user(
            token,
            TokenTest.user_info['HTTP_APP_ID'],
            TokenTest.user_info['HTTP_APP_SECRET'],
            TokenTest.user_info['HTTP_REDIRECT_URL']
        )
        query_set = User.objects.all()
        assert_that(len(query_set), 1)
        redis_token = redis.get(f'user:{meli_id}')
        assert_that(json.loads(redis_token).get('access_token'), is_not('BOGUS'))
        assert_that(json.loads(redis_token), json.dumps(token))

    def __create_mock_user(self):
        user = User(
            app_id=TokenTest.user_info['HTTP_APP_ID'],
            app_secret=TokenTest.user_info['HTTP_APP_SECRET'],
            meli_id=TokenTest.user_info['HTTP_MELI_ID']
        )
        user.save()
