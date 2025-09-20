from django.urls import path
from . import views

app_name='posts'

urlpatterns = [
    path('',views.posts_list,name="list"), # We are already in posts path so we are writing '' instead of '/posts'
    path('<slug:slug>',views.posts_page,name="page"), # Using path convertor

]