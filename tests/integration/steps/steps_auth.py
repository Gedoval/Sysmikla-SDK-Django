import configparser
import json
import os
import requests
from behave import *
from utils import *
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
    user_data = convert_table_to_dict(context.table)
    headers = set_headers(user_data)
    url = config.get('DJANGO', 'BASE_URL') + config.get('DJANGO', 'NEW_TOKEN_PATH')
    response = requests.get(url=url, headers=headers)
    assert response.status_code == 200
    context.session = TestSession(meli_id=response.json().get('user_id'),
                                  access_token=response.json().get('access_token'))
    assert_that("access_token" in response.json(), True)


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
        print(e)
    cursor = cnx.cursor(buffered=True)
    fields = ','.join(Constants.USER_QUERY_FIELDS)
    query = f'SELECT {fields} FROM mercadolibre_user'
    cursor.execute(query)
    rows = cursor.fetchall()
    assert_that(len(rows), 1)
    cursor.close()
    cnx.close()


@then('A new Token should be generated and stored in Redis')
def save_token_in_redis(context):
    user_id = convert_table_to_dict(context.table).get('USER_ID')
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
