from django.db import models

class User(models.Model):

    meli_id = models.IntegerField(default=-1)
    sysmika_id = models.IntegerField(default=-1)
    app_id = models.CharField(max_length=500)
    app_secret = models.CharField(max_length=500)
    redirect_url = models.CharField(max_length=500, default='')

class RealState(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    operation = models.CharField(max_length=30)
    date = models.DateTimeField()
    successful = models.BooleanField(default=False)
    description = models.CharField(max_length=2000)
    publication_id = models.CharField(max_length=200)


