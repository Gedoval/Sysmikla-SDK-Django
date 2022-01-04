from django.urls import path

from . import views
from .constants import Constants as CONST

urlpatterns = [
    path(CONST.GET_ACCESS_TOKEN, views.AccessToken.as_view())
]

