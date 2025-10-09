from django.urls import path
from . import views

urlpatterns = [
    path('', views.favourite_post_page, name='favourite_post'),
]
