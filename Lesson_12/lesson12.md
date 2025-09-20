# Django Lesson 12: Custom Forms and Post Creation

## Overview
This lesson focuses on creating custom Django forms using ModelForm, implementing post creation functionality, handling file uploads, and establishing relationships between users and posts. We'll learn about form processing, author assignment, and advanced form handling techniques.

---

## 1. Creating Custom Forms with ModelForm

### NEW: `posts/forms.py`:
```python
from django import forms
from . import models

class CreatePost(forms.ModelForm):
    class Meta:
        model = models.Post  # from models.py
        fields = ['title', 'body', 'slug', 'banner']
```

**Key Concepts:**
- **NEW FILE**: `forms.py` created in posts app
- **ModelForm**: Django form based on a model
- **Meta class**: Configuration for the form
- **Model reference**: Links form to Post model
- **Field selection**: Only includes specified fields in the form

**ModelForm Benefits:**
- **Automatic field generation**: Django creates form fields based on model fields
- **Built-in validation**: Inherits model field validation rules
- **Easy saving**: Can save directly to database
- **Less code**: No need to define individual form fields

---

## 2. Enhanced Post Model with Author Relationship

### Changes to `posts/models.py`:

**Previous (Lesson 7):**
```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(default='fallback.png', blank=True)
```

**Updated (Lesson 12):**
```python
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=75)
    body = models.TextField()
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(default='fallback.png', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title
```

**Key Changes:**
- **User import**: `from django.contrib.auth.models import User`
- **Author field**: `models.ForeignKey(User, on_delete=models.CASCADE, default=None)`
- **Title length**: Changed from 200 to 75 characters
- **Relationship**: Links each post to a user

**ForeignKey Parameters:**
- **User**: References Django's built-in User model
- **on_delete=models.CASCADE**: Delete posts when user is deleted
- **default=None**: Allows existing posts without authors

---

## 3. Complete Post Creation View

### Enhanced `posts/views.py`:

**Previous (Lesson 11):**
```python
from django.shortcuts import render
from .models import Post 
from django.contrib.auth.decorators import login_required

@login_required(login_url="/users/login/")
def posts_new(request):
    return render(request, 'posts/post_new.html')
```

**Updated (Lesson 12):**
```python
from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from . import forms 

def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'posts/posts_list.html', {'posts': posts})

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'posts/post_page.html', {'post': post})

@login_required(login_url="/users/login/")
def post_new(request):
    if request.method == 'POST': 
        form = forms.CreatePost(request.POST, request.FILES) 
        if form.is_valid():
            newpost = form.save(commit=False) 
            newpost.author = request.user 
            newpost.save()
            return redirect('posts:list')
    else:
        form = forms.CreatePost()
    return render(request, 'posts/post_new.html', { 'form': form })
```

**New Features:**

### Form Import:
- **Custom forms**: `from . import forms`
- **Local import**: Uses forms from the same app

### Complete Form Handling:
- **GET request**: Display empty form
- **POST request**: Process form submission
- **File handling**: `request.FILES` for image uploads
- **Form validation**: `form.is_valid()` checks all field requirements

### Advanced Save Process:
- **commit=False**: `form.save(commit=False)` creates object without saving
- **Author assignment**: `newpost.author = request.user` sets current user as author
- **Manual save**: `newpost.save()` completes the save process
- **Success redirect**: Returns to posts list after successful creation

---

## 4. Enhanced Post Creation Template

### Updated `templates/posts/post_new.html`:
```html
{% extends 'layout.html' %}

{% block title %}
    New Post
{% endblock %}

{% block content %}
    <section>
        <h1>New Post</h1>
        <form class="form-with-validation" action="{% url 'posts:new-post' %}" method="post" enctype="multipart/form-data">
            {% csrf_token %}
            {{ form }}
            <button class="form-submit">Add Post</button>
        </form>
    </section>
{% endblock %}
```

**Key Template Features:**
- **File upload support**: `enctype="multipart/form-data"`
- **CSRF protection**: Required for POST forms
- **Form rendering**: `{{ form }}` displays all form fields
- **Action URL**: Points to named URL pattern

**Form Encoding Types:**
- **multipart/form-data**: Required for file uploads
- **application/x-www-form-urlencoded**: Default for text forms
- **File handling**: Django processes uploaded files automatically

---

## 5. URL Configuration Updates

### Changes to `posts/urls.py`:

**Previous (Lesson 11):**
```python
urlpatterns = [
    path('', views.posts_list, name="list"),
    path('new-post/', views.posts_new, name="new_post"),
    path('<slug:slug>', views.posts_page, name="page"),
]
```

**Updated (Lesson 12):**
```python
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.posts_list, name="list"),
    path('new-post/', views.post_new, name="new-post"),
    path('<slug:slug>', views.post_page, name="page"),
]
```

**Key Changes:**
- **Function names**: Updated to match actual view function names
- **URL name**: Changed from "new_post" to "new-post" (matches template)
- **Consistency**: View names and URL names aligned

---

## 6. Enhanced Templates with Author Display

### Updated `templates/posts/posts_list.html`:

**Previous (Lesson 6):**
```html
<article class="post">
    <h2>
        <a href="{% url 'posts:page' slug=post.slug %}">
            {{ post.title }}
        </a>
    </h2>
    <p>{{ post.date }}</p>
    <p>{{ post.body }}</p>
</article>
```

**Updated (Lesson 12):**
```html
{% extends 'layout.html' %}

{% block title %}
    Posts
{% endblock %}

{% block content %}
    <section>
        <h1>Posts</h1>
        {% for post in posts %}
            <article class="post">
                <h2>
                    <a href="{% url 'posts:page' slug=post.slug %}">
                        {{ post.title }}
                    </a>
                </h2>
                <p>{{ post.date }} by {{ post.author }}</p>
                <p>{{ post.body }}</p>
            </article>
        {% endfor %}
    </section>
{% endblock %}
```

**Author Display:**
- **Author information**: `by {{ post.author }}` shows post author
- **User relationship**: Displays the username of the post creator
- **Attribution**: Clear indication of who wrote each post

### Enhanced `templates/posts/post_page.html`:

**Updated with image styling:**
```html
{% extends 'layout.html' %}

{% block title %}
    {{ post.title }}
{% endblock %}

{% block content %}
    <section>
        <img 
            class="banner"
            src="{{ post.banner.url }}"
            alt="{{ post.title }}"
        />
        <h1>{{ post.title }}</h1>
        <p>{{ post.date }}</p>
        <p>{{ post.body }}</p>
    </section>
{% endblock %}
```

**Image Enhancements:**
- **CSS class**: `class="banner"` for styling
- **Responsive design**: Better image presentation
- **Accessibility**: Proper alt attribute

---

## 7. Form Processing Flow

### Complete Post Creation Process:

1. **User clicks "New Post"** → GET `/posts/new-post/`
2. **Django displays form** → Empty CreatePost form
3. **User fills form** → Title, body, slug, banner
4. **User submits form** → POST with form data and files
5. **Django validates** → Check all field requirements
6. **Form saves** → `commit=False` creates object in memory
7. **Author assigned** → `newpost.author = request.user`
8. **Object saved** → `newpost.save()` commits to database
9. **User redirected** → Returns to posts list

```
Form Display → User Input → Form Submission → Validation → Author Assignment → Save → Redirect
```

---

## 8. Advanced Form Concepts

### commit=False Pattern:
```python
newpost = form.save(commit=False)
newpost.author = request.user
newpost.save()
```

**Why Use commit=False:**
- **Partial save**: Creates object without database commit
- **Additional processing**: Allows modification before saving
- **Required fields**: Can set fields not in the form
- **Data integrity**: Ensures all required relationships are set

### File Upload Handling:
```python
form = forms.CreatePost(request.POST, request.FILES)
```

**File Processing:**
- **request.POST**: Contains form text data
- **request.FILES**: Contains uploaded files
- **Automatic handling**: Django processes file uploads automatically
- **Validation**: ImageField validates file types

---

## 9. Database Relationships

### ForeignKey Relationship:
```python
author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
```

**Relationship Benefits:**
- **Data integrity**: Ensures posts are linked to users
- **Query efficiency**: Can retrieve user info with posts
- **Cascade delete**: Removes posts when user is deleted
- **Admin integration**: Shows relationships in Django admin

### Accessing Related Data:
```python
# In templates
{{ post.author }}  # Shows username
{{ post.author.email }}  # Shows user email
{{ post.author.first_name }}  # Shows first name

# In views
user_posts = Post.objects.filter(author=request.user)
```

---

## 10. Form Security and Validation

### Built-in Security:
- **CSRF protection**: Required for all POST forms
- **File validation**: ImageField validates file types
- **Field validation**: CharField, TextField validate input
- **Model validation**: Model constraints enforced

### Form Validation Process:
1. **Field validation**: Each field checked individually
2. **Model validation**: Model constraints checked
3. **Custom validation**: Any custom clean methods
4. **Error collection**: All errors collected and displayed
5. **Success handling**: Valid forms processed and saved

---

## Key Concepts Learned

### Custom Forms:
- **ModelForm**: Django forms based on models
- **Meta class**: Form configuration
- **Field selection**: Choosing which fields to include
- **Automatic validation**: Inheriting model validation

### File Uploads:
- **multipart/form-data**: Required encoding for file uploads
- **request.FILES**: Handling uploaded files
- **ImageField**: Specialized field for image uploads
- **Media configuration**: Proper file storage setup

### Database Relationships:
- **ForeignKey**: Linking models together
- **User model**: Using Django's built-in User model
- **Cascade deletion**: Handling related object deletion
- **Author assignment**: Linking posts to users

### Advanced Techniques:
- **commit=False**: Partial form saving
- **Manual field assignment**: Setting fields not in forms
- **Form processing**: Complete GET/POST handling
- **User context**: Using request.user in views

---

## Next Steps

After mastering custom forms, you're ready for:
- **Form customization and styling**
- **Advanced form validation**
- **Inline formsets**
- **AJAX form processing**
- **File upload improvements**

You now have a complete blog system with user-created content and proper author attribution!