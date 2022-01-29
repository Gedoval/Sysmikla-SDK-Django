from django.urls import path
from . import views
from .constants import Constants as CONST

urlpatterns = [
    path(CONST.GET_ACCESS_TOKEN, views.AccessTokenAPI.as_view(), name='get-token'),
    path(CONST.CREATE_TEST_USER, views.MercadoLibreTestContext.as_view(), name='create-test-user'),
    path(CONST.CATEGORY, views.MercadoLibreCategories.as_view(), name='get-category'),
    path(CONST.CATEGORY_ATTRIBUTES, views.MercadoLibreCategoriesAttributes.as_view(), name='get-category-attributes'),
    path(CONST.SITE_CATEGORIES, views.MercadoLibreSiteCategories.as_view(), name='get-site-categories'),
    path(CONST.CREATE_PUBLICATION, views.MercadoLibreRealStatePublications.as_view(), name='realstate-insert')
]

