from rest_framework import serializers

from .models import AccessToken, RealState, User


class AccessTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessToken
        fields = ['id', 'access_token', 'token_type', 'expires_in', 'user_id', 'refresh_token']

class UserSerializer(serializers.ModelSerializer):
    access_token = serializers.RelatedField(source='access_token', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'meli_id', 'sysmika_id', 'access_token', 'app_id', 'app_secret']
