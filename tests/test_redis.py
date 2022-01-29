from apps.redis.handler import RedisHandler
from pathlib import Path
import json
from hamcrest import *


class TestRedis:
    BASE_DIR = Path(__file__).resolve().parent.parent
    r = RedisHandler()

    def test_set_redis(self):
        token = json.load(open(str(TestRedis.BASE_DIR) + "/tests/resources/mock_token.json"))
        result = TestRedis.r.setex('hola', token)
        assert_that(result == 0, True)

    def test_get_redis(self):
        token = json.load(open(str(TestRedis.BASE_DIR) + "/tests/resources/mock_token.json"))
        result = TestRedis.r.setex('hola', token)
        assert_that(result == 0, True)
        result = TestRedis.r.get('hola')
        assert_that(result, not_none())

    def test_get_redis_empty(self):
        result = TestRedis.r.get('empty')
        assert_that(result is None, True)

    def test_iter_over_keys(self):
        for key in TestRedis.r.scan_iter('*'):
            print(key)

    def test_sets(self):
        result = TestRedis.r.lock_user('test')
        assert_that(result, same_instance(1))
        result = TestRedis.r.unlock_user('test')
        assert_that(result, same_instance(1))
        result = TestRedis.r.clear_lock_set()
        assert_that(result, same_instance(0))


