import json
from pathlib import Path
from rest_framework.test import APITestCase
from django.urls import reverse
from apps.mercadolibre.constants import Constants as Consts
from apps.mercadolibre.models import AccessToken, User
import requests_mock
from hamcrest import *
from rest_framework import status
from apps.mercadolibre.serializers import AccessTokenSerializer, UserSerializer


class TokenTest(APITestCase):
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
            token_obj = AccessToken.objects.all().values()
            user_obj = User.objects.all().values()
            assert_that(len(token_obj), 1)
            assert_that(len(user_obj), 1)
            user = UserSerializer(data=user_obj[0])
            token = AccessTokenSerializer(data=token_obj[0])
            assert_that(user.is_valid(), True, user.errors)
            assert_that(token.is_valid(), True, token.errors)
