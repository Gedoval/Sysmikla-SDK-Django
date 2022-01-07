from rest_framework import serializers

from .models import AccessToken, RealState, User


class AccessTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessToken
        fields = ['id', 'access_token', 'token_type', 'expires_in', 'user_id', 'refresh_token']


class UserSerializer(serializers.ModelSerializer):

    @staticmethod
    def populate_user(meli_id, app_id, app_secret, sysmika_id=None):
        user = dict()
        user['meli_id'] = meli_id
        if sysmika_id is None:
            user['sysmika_id'] = -1
        else:
            user['sysmika_id'] = sysmika_id
        user['app_id'] = app_id
        user['app_secret'] = app_secret
        return user

    class Meta:
        model = User
        fields = ['id', 'meli_id', 'sysmika_id', 'app_id', 'app_secret']
