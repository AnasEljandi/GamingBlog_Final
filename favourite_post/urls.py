from django.urls import path
from .views import favourite_post_page
from . import views

urlpatterns = [
    path('', views.favourite_post_page, name='favourite_post'),
]
