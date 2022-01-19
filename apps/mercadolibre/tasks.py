from apps.mercadolibre.serializers import UserSerializer
from apps.mercadolibre.models import User
from conf.celery import app
from conf.settings import r as redis
import json
from datetime import timedelta


@app.task
def store_token_and_user(token, app_id, app_secret, redirect_url):
    user = UserSerializer.populate_user(
        meli_id=token.get('user_id'),
        app_secret=app_secret,
        app_id=app_id,
        redirect_url=redirect_url
    )
    query_set = User.objects.filter(meli_id=token.get('user_id')).first()
    if query_set is None:
        user_seri = UserSerializer(data=user)
        if user_seri.is_valid():
            user_seri.save()
        else:
            raise NotImplementedError  # TODO
    save_token(token['user_id'], token)
    return json.dumps(token)


def save_token(meli_id, token):
    redis.setex(
        f'user:{meli_id}',
        timedelta(hours=6),
        value=json.dumps(token)
    )
