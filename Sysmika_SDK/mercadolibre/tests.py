import django
from django.test import TestCase
from django.test import Client
import requests_mock
from pathlib import Path
import json
from constants import Constants as CONST
from Sysmika_SDK.Sysmika_SDK import settings
import unittest

class Algo(unittest.TestCase):
    BASE_DIR = Path(__file__).resolve().parent.parent
    settings.configure()
    def test_get_token(self):
        headers = {
            CONST.TG_CODE: "TG-1234",
            CONST.REDIRECT_URL: "http://asd.com",
            CONST.APP_ID: "APP-ID",
            CONST.APP_SECRET: "APP-Secret"
        }
        Client().post(
            data=json.load(open(str(Algo.BASE_DIR) + "/resources/mock_token.json")),
            path=CONST.GET_ACCESS_TOKEN
        )

