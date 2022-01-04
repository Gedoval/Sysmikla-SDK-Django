import requests
from rest_framework import status
from rest_framework.response import Response

from .constants import Constants as CONST


class MercadoLibreInvoker:

    def __init__(self):
        pass

    def get_access_token(self, app_id, app_secret, tg_code, request_url):

        headers = {"content-type": "application/x-www-form-urlencoded", "accept": "application/json"}
        body = self.create_token_request_body(app_id, app_secret, tg_code, request_url)
        response = requests.post(CONST.API_HOST + CONST.TOKEN_URL, data=body, headers=headers)
        return response.json()


    def create_token_request_body(self, app_id, app_secret, tg_code, redirect_url):
        return "grant_type=authorization_code&" \
               "client_id=" + app_id + "&" \
               "client_secret=" + app_secret + "&" \
                "code=" + tg_code + "&" \
                "redirect_uri=" + redirect_url

