from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .constants import Constants as CONST
from .invoker import MercadoLibreInvoker
from .exceptions import *
import apps.mercadolibre.tasks as tasks
from pathlib import Path
from jsonschema import validate, ValidationError
import json

"""Generic endpoints. We can use these no matter what type of customer is calling the API, i.e a realstate user, 
vehicles user, etc.
"""
sync_schema = json.load(open(str(Path(__file__).resolve().parent) + '/resources/sync_event.json'))


def validate_sync_event_schema(data, schema):
    remove = ("$id", "$schema", "description", "title")
    for k in remove:
        schema.pop(k, None)
    try:
        validate(instance=json.loads(data), schema=schema)
    except ValidationError:
        return False
    return True


class AccessTokenAPI(APIView):
    def get(self, request):
        if not all(key in request.headers for key in (
                CONST.TG_CODE, CONST.REDIRECT_URL, CONST.APP_ID, CONST.APP_SECRET
        )):
            return Response("Missing required headers", status=status.HTTP_400_BAD_REQUEST)
        try:
            access_token = MercadoLibreInvoker().get_access_token(
                request.headers[CONST.APP_ID],
                request.headers[CONST.APP_SECRET],
                request.headers[CONST.TG_CODE],
                request.headers[CONST.REDIRECT_URL]
            )
        except BadTokenException as e:
            return Response(e.message, status=status.HTTP_401_UNAUTHORIZED)
        except ServiceUnavailable as e:
            return Response(e.get_full_details(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        tasks.store_token_and_user.delay(
            access_token,
            request.headers[CONST.APP_ID],
            request.headers[CONST.APP_SECRET],
            request.headers[CONST.REDIRECT_URL]
        )
        return Response(access_token, status=status.HTTP_200_OK)

class MercadoLibreRealStatePublications(APIView):

    def post(self, request):
        if CONST.USER_ID not in request.headers:
            return Response("Missing required headers", status=status.HTTP_400_BAD_REQUEST)

        if validate_sync_event_schema(request.data, sync_schema) is False:
            return Response('Sync Event schema not honored', status=status.HTTP_400_BAD_REQUEST)
        try:
            response = MercadoLibreInvoker().post_publication(request)
            if response.status_code != 200:
                return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(response.json(), status=status.HTTP_200_OK)
        except NoSuchUserException as n:
            return Response(n.__repr__(), status=status.HTTP_401_UNAUTHORIZED)


class MercadoLibreCategories(APIView):

    def get(self, request, category_id):
        try:
            response_code = status.HTTP_200_OK
            response = MercadoLibreInvoker().get_category(category_id)
        except ServiceUnavailable as e:
            response = e.get_full_details()
            response_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return Response(response, status=response_code)


class MercadoLibreCategoriesAttributes(APIView):

    def get(self, request, category_id):
        try:
            response_code = status.HTTP_200_OK
            response = MercadoLibreInvoker().get_category(category_id, True)
        except ServiceUnavailable as e:
            response = e.get_full_details()
            response_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return Response(response, status=response_code)


class MercadoLibreSiteCategories(APIView):

    def get(self, request, site):
        try:
            response_code = status.HTTP_200_OK
            return Response(MercadoLibreInvoker().get_site_categories(site), status=response_code)
        except ServiceUnavailable as e:
            response = e.get_full_details()
            response_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return Response(response, status=response_code)


class MercadoLibreTestContext(APIView):

    def get(self, request):
        if not all(key in request.headers for key in (
                CONST.APP_TOKEN, CONST.SITE
        )):
            return Response("Missing required headers", status=status.HTTP_400_BAD_REQUEST)
        try:

            test_user = MercadoLibreInvoker().create_test_user(
                request.headers[CONST.APP_TOKEN],
                request.headers[CONST.SITE]
            )
        except BadTokenException as e:
            return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
        except ServiceUnavailable as e:
            return Response(e.get_full_details(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return test_user
