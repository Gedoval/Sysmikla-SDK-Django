from apps.mercadolibre.serializers import UserSerializer
from apps.mercadolibre.models import User
from apps.mercadolibre.invoker import MercadoLibreInvoker
from conf.celery import app
from apps.redis.handler import RedisHandler

redis = RedisHandler()


@app.task(bind=True)
def store_token_and_user(self, token, app_id, app_secret, redirect_url):
    user = {
        'meli_id': token.get('user_id'),
        'app_id': app_id,
        'app_secret': app_secret,
        'redirect_url': redirect_url,
        'access_token': token.get('access_token'),
        'refresh_token': token.get('refresh_token')
    }

    query_set = User.objects.filter(meli_id=token.get('user_id')).first()
    if query_set is None:
        user_seri = UserSerializer(data=user)
        if user_seri.is_valid():
            user_seri.save()
            redis.setex('user:' + str(token['user_id']), token)
        else:
            redis.setex('user_error:' + str(token['user_id']), user_seri.errors)
    else:
        redis.setex('user:' + str(token['user_id']), token)
    return None


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(1.0, refresh_token)


@app.task(bind=True)
def refresh_token():
    raise NotImplemented
    # key_prefix = '_*'
    # invoker = MercadoLibreInvoker()
    # for key in redis.scan_iter(key_prefix):
    #     ttl = redis.ttl(key)
    #     if ttl <= 3600:
    #         value = redis.get(key)
    #         invoker.refresh_access_token(
    #             value.get('refresh_token'),
    #             value.get('app_id'),
    #             value.get('app_secret')
    #         )



