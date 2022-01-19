from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        query_set = User.objects.filter(meli_id=validated_data['meli_id']).values()
        if len(query_set) > 0:
            return validated_data
        else:
            return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.access_token = validated_data.get('access_token', instance.access_token)
        instance.save()
        return instance



    @staticmethod
    def populate_user(meli_id, app_id, app_secret, redirect_url, sysmika_id=None):
        user = dict()
        user['meli_id'] = meli_id
        if sysmika_id is None:
            user['sysmika_id'] = -1
        else:
            user['sysmika_id'] = sysmika_id
        user['app_id'] = app_id
        user['app_secret'] = app_secret
        user['redirect_url'] = redirect_url
        return user

    class Meta:
        model = User
        fields = ['id', 'meli_id', 'sysmika_id', 'app_id', 'app_secret']
