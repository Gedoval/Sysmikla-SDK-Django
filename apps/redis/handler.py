import redis
import json
from datetime import timedelta
from conf.settings import REDIS


class RedisHandler:
    def __init__(self):
        self.redis = redis.Redis(
            host=REDIS.get('REDIS_HOST'),
            port=REDIS.get('REDIS_PORT'),
            db=REDIS.get('REDIS_DB')
        )

    def lock(self, set_name, value):
        """
        Creates a Redis Set that serves as a 'locking' reference: we store ID's of in-transit users to avoid
        potential collision. For example, if a Django User has a request in flight and we attempt to renew his access
        token via a Celery scheduler, we can potentially break the User authentication.
         :param set_name: name of the Set to serve as locking set
         :param value: value to store in the Set. It should be some form of ID
         :return: 1 if the set was created/updated successfully or None otherwise.
        """
        try:
            return self.redis.sadd(set_name, value)
        except BaseException as e:
            raise NotImplemented  # TODO

    def unlock(self, set_name, value):
        """
        Removes a value from a locking Set
         :param set_name: name of the locking Set
         :param value: the value to remove. Usually some form of ID
         :return: 1 if the value exists. None otherwise
        """
        try:
            return self.redis.srem(set_name, value)
        except BaseException as e:
            raise NotImplemented  # TODO

    def clear_set(self, set_name):
        try:
            return self.redis.delete(set_name)
        except BaseException as e:
            raise NotImplemented  # TODO

    def is_in_set(self, set_name, value):
        return self.redis.sismember(set_name, value)

    def setex(self, key, value, time=timedelta(hours=6)):
        try:
            self.redis.setex(
                key,
                time,
                value=self.__to_redis(value)
            )
            return 0
        except BaseException as e:
            # TODO
            pass

    def get(self, key):
        try:
            return self.__from_redis(self.redis.get(key))
        except BaseException as e:
            # TODO
            pass

    def get_user_token(self, user_id):
        try:
            user = self.get(user_id)
            if user is None:
                return None
            else:
                return user.get('access_token')
        except BaseException as e:
            raise NotImplemented  # TODO

    def scan_iter(self, key):
        return self.redis.scan_iter(key)

    def ttl(self, key):
        return self.redis.ttl(key)

    def __to_redis(self, data):
        return json.dumps(data)

    def __from_redis(self, data):
        return json.loads(data)
