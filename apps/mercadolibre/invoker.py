import requests
import time
from .constants import Constants as CONST
from apps.redis.handler import RedisHandler
from pathlib import Path
from conf import settings
from apps.mercadolibre.models import User
from apps.mercadolibre.exceptions import *


class MercadoLibreInvoker:

    def __init__(self):
        self.headers = {"content-type": "application/x-www-form-urlencoded", "accept": "application/json"}
        self.redis = RedisHandler()
        self.base_dir = Path(__file__).resolve().parent

    def get_access_token(self, app_id, app_secret, tg_code, request_url):
        try:
            body = self.create_token_request_body(app_id, app_secret, tg_code, request_url)
            response = requests.post(CONST.API_HOST + CONST.TOKEN_URL, data=body, headers=self.headers)
            print(response.json())
        except BaseException as e:
            raise ServiceUnavailable
        if response.status_code != 200:
            raise BadTokenException(response.json())
        return response.json()

    def refresh_access_token(self, refresh_token, app_id, app_secret):
        try:
            body = self.refresh_token_request_body(refresh_token, app_id, app_secret)
            response = requests.post(CONST.API_HOST + CONST.TOKEN_URL, data=body, headers=self.headers)
        except BaseException:
            raise ServiceUnavailable
        if response.status_code != 200:
            raise BadTokenException(response.json())
        return response.json()

    def get_category(self, category_id, attributes=False):
        url = CONST.API_HOST + CONST.CATEGORIES + '/' + category_id
        key = category_id
        if attributes:
            key = key + ':attributes'
            category = self.redis.get(key)
            url = url + '/attributes'
        else:
            category = self.redis.get(key)
        if category is None:
            try:
                category = requests.get(url).json()
            except BaseException:
                raise ServiceUnavailable
            if isinstance(category, list) or 'error' not in category.keys():
                self.redis.setex(key, category)
        return category

    def get_site_categories(self, site):
        categories = self.redis.get(f'{site}:categories')
        if categories is None:
            try:
                url = CONST.API_HOST + '/' + CONST.SITES + '/' + site + '/categories'
                categories = requests.get(url).json()
            except BaseException:
                raise ServiceUnavailable

            if isinstance(categories, list) or 'error' not in categories.keys():
                self.redis.setex(f'{site}:categories', categories)
        return categories

    def post_publication(self, request):
        try:
            access_token = self.__get_context_user(request.headers['user-id'])
        except NoSuchUserException as e:
            raise e
        headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
        url = CONST.API_HOST + CONST.ITEMS
        body = request.data
        response = requests.post(url, json=body, headers=headers)
        self.redis.unlock(CONST.USER_LOCK, request.headers['user-id'])
        return response

    # def delete_publication(self, item_id):
    #     headers = {"Authorization": "Bearer " + self.builder.get_app_token(),
    #                "Content-Type": "application/json",
    #                "Accept": "application/json"
    #                }
    #     body = {"deleted": "true"}
    #     client = self.make_put_request(
    #         Consts.API_HOST,
    #         Consts.ITEMS + "/" + item_id,
    #         body=body,
    #         headers=headers
    #     )
    #     response = requests.put(client.host + client.url, json=client.post_body)
    #     if response.status_code != 200:
    #         raise SysmikaUtils.json_parser(response.json(), PublicationError())
    #     return SysmikaUtils.json_parser(response.json(), ApiResponse())

    def create_test_user(self, app_token, site):
        headers = {"Authorization": "Bearer " + app_token, "Content-Type": "application/json"}
        site_body = '{"site_id":' + '"' + site + '"' + '}'
        return 'asd'

    def create_token_request_body(self, app_id, app_secret, tg_code, redirect_url):
        return "grant_type=authorization_code&" \
               "client_id=" + app_id + "&" \
                                       "client_secret=" + app_secret + "&" \
                                                                       "code=" + tg_code + "&" \
                                                                                           "redirect_uri=" + redirect_url

    def refresh_token_request_body(self, refresh_token, app_id, app_secret):
        return "grant_type=refresh_token&" \
               "client_id=" + app_id + "&" \
                                       "client_secret=" + app_secret + "&" \
                                                                       "refresh_token=" + refresh_token

    def __get_context_user(self, user_id):
        """
        Retrieves the access token of the user that initiated the request. Two checks are used: first we look for the user on Redis,
        and if not found there we call the Django DB. If no user is found, an Unauthorized exception is thrown back to the caller.
        :param user_id: the MercadoLibre ID of the User
        :return: an access token or None if no User was found
        """
        try:
            access_token = self.redis.get_user_token(user_id)
            if access_token is None:
                query_set = User.objects.filter(meli_id=user_id).first()
                if query_set is None:
                    raise NoSuchUserException(user_id)
                else:
                    access_token = query_set.access_token
                    self.redis.setex('user:' + str(user_id), access_token)
            self.__assert_unlocked_user(user_id)
            self.redis.lock(CONST.USER_LOCK, user_id)
            return access_token
        except NoSuchUserException as e:
            raise e

    def __assert_unlocked_user(self, user_id):
        while self.redis.is_in_set(CONST.USER_LOCK, user_id):
            time.sleep(int(CONST.POLLING_INTERVAL))
