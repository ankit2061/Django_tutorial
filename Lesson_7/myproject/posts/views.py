from django.shortcuts import render
from .models import Post #new import


# Create your views here.
def posts_list(request):
    posts=Post.objects.all().order_by('-date') #referred from the previous ORM lecture and added the order_by constraint date
    return render(request,'posts/posts_list.html',{'posts':posts})# we added the extra parameter of dictionary here
'''
So whats basically we are doing here?
We are bringing in 'Post' model -> 
we are getting all of the posts -> 
passing all of that data on to the template
'''
def posts_page(request,slug):
    post=Post.objects.get(slug=slug)
    return render(request,'posts/post_page.html',{'post':post})# we added the extra parameter of dictionary here
