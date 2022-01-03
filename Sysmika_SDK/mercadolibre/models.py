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
    access_token = models.ForeignKey(AccessToken, on_delete=models.CASCADE, default=-1)
    app_id = models.CharField(max_length=500)
    app_secret = models.CharField(max_length=500)

    def populate_user(self, meli_id, access_token, app_id, app_secret, sysmika_id=None):
        self.meli_id = meli_id
        if sysmika_id is None:
            self.sysmika_id = -1
        else:
            self.sysmika_id = sysmika_id
        self.app_id = app_id
        self.app_secret = app_secret
        if isinstance(access_token, AccessToken):
            self.access_token = access_token
        else:
            a_token = AccessToken()
            for k, v in access_token.items():
                try:
                    setattr(a_token, k, v)
                except:
                    pass
            self.access_token = a_token

class RealState(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    operation = models.CharField(max_length=30)
    date = models.DateTimeField()
    successful = models.BooleanField(default=False)
    description = models.CharField(max_length=2000)
    publication_id = models.CharField(max_length=200)


