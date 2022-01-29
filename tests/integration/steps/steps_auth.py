import configparser
import json
import os
import time
import requests
from behave import *
import utils as Util
import mysql.connector
from hamcrest import *
import redis

config = configparser.ConfigParser()
config.read(
    os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-1]) + '/config.properties')
DB = 'MYSQL'
REDIS = 'REDIS'
r = redis.Redis(
    host=config.get(REDIS, 'REDIS_HOST'),
    port=config.get(REDIS, 'REDIS_PORT'),
    db=config.get(REDIS, 'REDIS_DB')
)


@when('A new user requires a new Token with the following data')
def new_user_registration(context):
    user_data = Util.convert_table_to_dict(context.table)
    headers = set_headers(user_data)
    url = config.get('DJANGO', 'BASE_URL') + config.get('DJANGO', 'NEW_TOKEN_PATH')
    response = requests.get(url=url, headers=headers)
    assert response.status_code == 200
    assert_that(response.json(), has_key('access_token'))
    context.session = Util.TestSession(meli_id=response.json().get('user_id'),
                                  access_token=response.json().get('access_token'))


@then('A new User should be stored on the Django database with the following values')
def store_new_user(context):
    try:
        cnx = mysql.connector.connect(
            user=config.get(DB, 'USER'),
            password=config.get(DB, 'PASSWORD'),
            host=config.get(DB, 'HOST'),
            database=config.get(DB, 'DATABASE')
        )
    except mysql.connector.Error as e:
        print(f'Connection to DB failed {e}')
    cursor = cnx.cursor(buffered=True)
    fields = ','.join(Util.Constants.USER_QUERY_FIELDS)
    query = f'SELECT {fields} FROM mercadolibre_user'
    time.sleep(2)
    cursor.execute(query)
    rows = cursor.fetchall()
    assert_that(rows, has_length(1))
    cursor.close()
    cnx.close()


@then('A new Token should be generated and stored in Redis')
def save_token_in_redis(context):
    user_id = Util.convert_table_to_dict(context.table).get('USER_ID')
    user_key = f'user:{user_id}'
    token = r.get(user_key)
    assert_that(token, not_none())


def set_headers(data):
    return {
        'tg-code': data['TG_CODE'],
        'redirect-url': data['REDIRECT_URL'],
        'app-id': data['APP_ID'],
        'app-secret': data['APP_SECRET']
    }
