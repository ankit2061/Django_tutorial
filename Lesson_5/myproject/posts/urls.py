from django.urls import path
from . import views

urlpatterns = [
    path('',views.posts_list), # We are already in posts path so we are writing '' instead of '/posts'
]