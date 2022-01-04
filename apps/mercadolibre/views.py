from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import Constants as CONST
from .invoker import MercadoLibreInvoker
from .models import User
from .serializers import AccessTokenSerializer, UserSerializer


class AccessToken(APIView):
    def get(self, request):
        if not all(key in request.headers for key in (
                CONST.TG_CODE, CONST.REDIRECT_URL, CONST.APP_ID, CONST.APP_SECRET
        )):
            return Response("Missing required headers", status=status.HTTP_400_BAD_REQUEST)
        access_token = MercadoLibreInvoker().get_access_token(
            request.headers[CONST.APP_ID],
            request.headers[CONST.APP_SECRET],
            request.headers[CONST.TG_CODE],
            request.headers[CONST.REDIRECT_URL]
        )
        seri = AccessTokenSerializer(data=access_token)
        if seri.is_valid():
            seri.save()
            user = User().populate_user(
                meli_id=seri.data.get('user_id'),
                access_token=access_token,
                app_secret=request.headers[CONST.APP_SECRET],
                app_id=request.headers[CONST.APP_ID]
            )
            user_seri = UserSerializer(data=user)
            if user_seri.is_valid():
                user_seri.save()
            else:
                print(user_seri.errors)
            return Response(seri.data, status=status.HTTP_200_OK)
        else:
            return Response(access_token, status=status.HTTP_404_NOT_FOUND)

    def __prepare_user(self, data):
        user = User()
        user.access_token = data['access_token']
        user.app_id
        return user


