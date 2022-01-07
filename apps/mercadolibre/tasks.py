from apps.mercadolibre.serializers import AccessTokenSerializer, UserSerializer
from conf.celery import app
from .constants import Constants as CONST
import json


@app.task
def store_token_and_user(token, app_id, app_secret):
    seri = AccessTokenSerializer(data=token)
    if seri.is_valid():
        seri.save()
        user = UserSerializer.populate_user(
            meli_id=seri.data.get('user_id'),
            app_secret=app_secret,
            app_id=app_id
        )
        user_seri = UserSerializer(data=user)
        if user_seri.is_valid():
            user_seri.validated_data['access_token_id'] = seri.data['id']
            user_seri.save()
        else:
            pass
    return json.dumps(token)

