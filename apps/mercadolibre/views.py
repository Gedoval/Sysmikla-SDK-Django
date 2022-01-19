from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .constants import Constants as CONST
from .invoker import MercadoLibreInvoker
from .exceptions import BadTokenException
import apps.mercadolibre.tasks as tasks


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
            return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
        tasks.store_token_and_user.delay(
            access_token,
            request.headers[CONST.APP_ID],
            request.headers[CONST.APP_SECRET],
            request.headers[CONST.REDIRECT_URL]
        )
        return Response(access_token, status=status.HTTP_200_OK)

