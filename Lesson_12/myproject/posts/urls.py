from django.urls import path
from . import views

app_name='posts'

urlpatterns = [
    path('',views.posts_list,name="list"), # We are already in posts path so we are writing '' instead of '/posts'
    path('new-post/',views.post_new,name="new-post"),
    path('<slug:slug>',views.post_page,name="page"), # Using path convertor

]