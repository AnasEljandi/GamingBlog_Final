from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path("create/", views.post_create, name="post_create"),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('comment/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('favourite/<int:post_id>/toggle/', views.toggle_favourite, name='toggle_favourite'),
    path("<slug:slug>/delete/", views.post_delete, name="post_delete"),
   
]
