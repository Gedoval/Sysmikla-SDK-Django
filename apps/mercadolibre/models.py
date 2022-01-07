from django.db import models

class AccessToken(models.Model):
    access_token = models.CharField(max_length=500)
    token_type = models.CharField(max_length=100)
    expires_in = models.IntegerField(default=0)
    user_id = models.IntegerField(default=-1)
    refresh_token = models.CharField(max_length=500)


class User(models.Model):

    meli_id = models.IntegerField(default=-1)
    sysmika_id = models.IntegerField(default=-1)
    access_token = models.ForeignKey(AccessToken, on_delete=models.CASCADE)
    app_id = models.CharField(max_length=500)
    app_secret = models.CharField(max_length=500)


class RealState(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    operation = models.CharField(max_length=30)
    date = models.DateTimeField()
    successful = models.BooleanField(default=False)
    description = models.CharField(max_length=2000)
    publication_id = models.CharField(max_length=200)


