from django.urls import path

from . import views
from .constants import Constants as CONST

urlpatterns = [
    path(CONST.GET_ACCESS_TOKEN, views.AccessTokenAPI.as_view(), name='get-token')
]

