# Complete Django Learning Guide

## Table of Contents
1. [Introduction to Django](#introduction)
2. [Project Setup & Configuration](#setup)
3. [Models & Database](#models)
4. [Views & URL Routing](#views)
5. [Templates & Static Files](#templates)
6. [Django Admin Interface](#admin)
7. [User Authentication & Authorization](#auth)
8. [Forms & File Uploads](#forms)
9. [Best Practices & Workflows](#best-practices)

---

## Introduction to Django {#introduction}

Django is a high-level Python web framework that follows the MTV (Model-Template-View) pattern, enabling rapid development of secure and maintainable websites.

### Core Philosophy
- **DRY (Don't Repeat Yourself)**: Minimize code repetition
- **Convention over Configuration**: Sensible defaults reduce boilerplate
- **Security by Default**: Built-in protection against common vulnerabilities
- **Scalability**: Designed to handle high traffic efficiently

---

## Project Setup & Configuration {#setup}

### Initial Project Creation

```bash
# Create virtual environment
python -m venv env_site
source env_site/bin/activate  # On Mac/Linux
env_site\Scripts\activate     # On Windows

# Install Django
pip install django

# Create project
django-admin startproject myproject
cd myproject

# Run development server
python manage.py runserver
```

### Project Structure
```
myproject/
├── myproject/          # Project configuration
│   ├── __init__.py
│   ├── settings.py     # Main configuration
│   ├── urls.py         # Root URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── manage.py           # Command-line utility
└── db.sqlite3          # Database (created after first migration)
```

### Creating Apps

```bash
python manage.py startapp posts
python manage.py startapp users
```

**Always register apps in `settings.py`:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'posts',    # Your apps
    'users',
]
```

### Static Files Configuration

```python
# settings.py
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
```

### Media Files Configuration

```python
# settings.py
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

```python
# Main urls.py
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # ... your patterns
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Models & Database {#models}

### Understanding Models

Models define your database structure. Each model is a Python class that represents a database table.

### Basic Model Example

```python
# posts/models.py
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

### Common Field Types

| Field Type | Use Case | Parameters |
|------------|----------|------------|
| `CharField` | Short text | `max_length` (required) |
| `TextField` | Long text | No length limit |
| `SlugField` | URL-friendly text | Lowercase, hyphens |
| `DateTimeField` | Date/time | `auto_now_add=True` for creation |
| `ImageField` | Images | Requires Pillow: `pip install Pillow` |
| `ForeignKey` | Relationships | Links to another model |
| `BooleanField` | True/False | Default values |
| `EmailField` | Email addresses | Built-in validation |

### Field Parameters

- **`max_length`**: Character limit (required for CharField)
- **`blank=True`**: Allows empty values in forms
- **`null=True`**: Allows NULL in database
- **`default`**: Default value
- **`unique=True`**: Ensures uniqueness
- **`auto_now_add=True`**: Set on creation
- **`auto_now=True`**: Update on every save

### Relationships

**ForeignKey (Many-to-One):**
```python
author = models.ForeignKey(User, on_delete=models.CASCADE)
```

**on_delete options:**
- `CASCADE`: Delete related objects
- `PROTECT`: Prevent deletion
- `SET_NULL`: Set to NULL
- `SET_DEFAULT`: Set to default value

### Migrations Workflow

```bash
# 1. Create migrations after model changes
python manage.py makemigrations

# 2. Apply migrations to database
python manage.py migrate

# Useful commands:
python manage.py showmigrations        # View migration status
python manage.py sqlmigrate posts 0001 # View SQL for migration
```

**Migration Best Practices:**
- Always create migrations after model changes
- Review migration files before applying
- Never edit applied migrations—create new ones
- Keep migrations in version control
- Test migrations on development database first

### Django ORM Basics

**Django Shell:**
```bash
python manage.py shell
```

**Basic Operations:**
```python
# Import model
from posts.models import Post

# Create object
p = Post()
p.title = "My First Post"
p.save()

# Query all objects
Post.objects.all()

# Get specific object
post = Post.objects.get(slug='my-slug')

# Filter objects
posts = Post.objects.filter(author=request.user)

# Order objects
posts = Post.objects.all().order_by('-date')  # Descending

# Count objects
Post.objects.count()
```

---

## Views & URL Routing {#views}

### View Functions

Views process HTTP requests and return HTTP responses.

**Basic View:**
```python
# posts/views.py
from django.shortcuts import render, redirect
from .models import Post

def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'posts/posts_list.html', {'posts': posts})

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'posts/post_page.html', {'post': post})
```

### URL Configuration

**App URLs (`posts/urls.py`):**
```python
from django.urls import path
from . import views

app_name = 'posts'  # Namespace

urlpatterns = [
    path('', views.posts_list, name="list"),
    path('new-post/', views.post_new, name="new-post"),
    path('<slug:slug>', views.post_page, name="page"),
]
```

**Project URLs (`myproject/urls.py`):**
```python
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
    path('users/', include('users.urls')),
    path('', views.Homepage),
    path('about/', views.about),
]
```

### Path Converters

- `<int:id>`: Matches integers
- `<str:name>`: Matches strings
- `<slug:slug>`: Matches slugs (letters, numbers, hyphens, underscores)
- `<path:path>`: Matches paths with slashes

### URL Naming & Reversing

**In templates:**
```html
<a href="{% url 'posts:list' %}">All Posts</a>
<a href="{% url 'posts:page' slug=post.slug %}">{{ post.title }}</a>
```

**Benefits:**
- Change URL patterns without updating templates
- Single source of truth
- Django validates URL names at runtime

### Important URL Ordering

Place specific URLs before general ones:
```python
urlpatterns = [
    path('new-post/', views.post_new, name="new-post"),  # Specific
    path('<slug:slug>', views.post_page, name="page"),   # General
]
```

---

## Templates & Static Files {#templates}

### Template Structure

```
myproject/
├── templates/          # Project-level templates
│   ├── layout.html    # Base template
│   ├── home.html
│   └── about.html
└── posts/
    └── templates/
        └── posts/      # App-level templates
            ├── posts_list.html
            ├── post_page.html
            └── post_new.html
```

### Base Template (`layout.html`)

```html
<!DOCTYPE html>
{% load static %}
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>
        {% block title %}
            Django App
        {% endblock %}
    </title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    <script src="{% static 'js/main.js' %}" defer></script>
</head>
<body>
    <nav>
        <a href="/"><span role="img" aria-label="Home" title="Home">🏠</span></a> |
        <a href="/about"><span role="img" aria-label="About" title="About">😊</span></a> |
        <a href="{% url 'posts:list' %}"><span role="img" aria-label="Posts" title="Posts">📰</span></a> |
        
        {% if user.is_authenticated %}
            <a href="{% url 'posts:new_post' %}"><span role="img" aria-label="New Post" title="New Post">🆕</span></a> |
            <form class="logout" action="{% url 'users:logout' %}" method="post">
                {% csrf_token %}
                <button class="logout-button" aria-label="User Logout" title="User Logout">👋</button>
            </form>
        {% else %}
            <a href="{% url 'users:register' %}"><span role="img" aria-label="User Registration" title="User Registration">🚀</span></a> |
            <a href="{% url 'users:login' %}"><span role="img" aria-label="User Login" title="User Login">🔐</span></a> |
        {% endif %}
    </nav>
    <main>
        {% block content %}
        {% endblock %}
    </main>
</body>
</html>
```

### Template Inheritance

```html
{% extends 'layout.html' %}

{% block title %}
    Posts
{% endblock %}

{% block content %}
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
{% endblock %}
```

### Template Tags & Filters

**Common Tags:**
- `{% extends 'base.html' %}`: Template inheritance
- `{% load static %}`: Load static files
- `{% block name %}`: Define replaceable blocks
- `{% for item in items %}`: Loop
- `{% if condition %}`: Conditional
- `{% url 'name' %}`: Reverse URL
- `{% csrf_token %}`: CSRF protection
- `{% comment %}`: Comments

**Common Filters:**
- `{{ value|length }}`: Length of string/list
- `{{ text|lower }}`: Lowercase
- `{{ date|date:"Y-m-d" }}`: Format date
- `{{ text|truncatewords:10 }}`: Truncate text

### Conditional Content

```html
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
{% else %}
    <p>Please log in.</p>
{% endif %}
```

### Image Display

```html
<img 
    class="banner"
    src="{{ post.banner.url }}"
    alt="{{ post.title }}"
/>
```

---

## Django Admin Interface {#admin}

### Creating Superuser

```bash
python manage.py createsuperuser
```

### Registering Models

```python
# posts/admin.py
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

### Admin Features

- **Automatic CRUD interface**: Create, Read, Update, Delete
- **Form generation**: Based on model fields
- **Search and filtering**: Built-in functionality
- **Bulk actions**: Operate on multiple records
- **User management**: Permissions and groups
- **Content management**: Non-technical users can manage data

### Accessing Admin

URL: `http://127.0.0.1:8000/admin/`

---

## User Authentication & Authorization {#auth}

### Authentication vs Authorization

**Authentication (Who you are):**
- Login/logout processes
- User identity verification
- Session management

**Authorization (What you can do):**
- Access control
- Permissions
- Conditional content

### User Registration

**Form:**
```python
# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())  # Auto-login
            return redirect("posts:list")
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {"form": form})
```

**Template:**
```html
{% extends 'layout.html' %}

{% block content %}
    <h1>Register a New User</h1>
    <form action="/users/register/" method="post">
        {% csrf_token %}
        {{ form }}
        <button type="submit">Submit</button>
    </form>
{% endblock %}
```

### User Login

```python
# users/views.py
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if "next" in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("posts:list")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {"form": form})
```

### User Logout

```python
from django.contrib.auth import logout

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("posts:list")
```

### Login Required Decorator

```python
from django.contrib.auth.decorators import login_required

@login_required(login_url="/users/login/")
def post_new(request):
    # Only authenticated users can access
    return render(request, 'posts/post_new.html')
```

### "Next" Parameter

Redirects users back to their intended page after login:

```python
if "next" in request.POST:
    return redirect(request.POST.get('next'))
```

### Accessing User in Views

```python
def my_view(request):
    if request.user.is_authenticated:
        user = request.user
        username = user.username
        # ...
```

### Accessing User in Templates

```html
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
    {{ user.email }}
    {{ user.first_name }}
{% endif %}
```

---

## Forms & File Uploads {#forms}

### ModelForm

ModelForm automatically generates forms from models.

```python
# posts/forms.py
from django import forms
from . import models

class CreatePost(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'body', 'slug', 'banner']
```

### Form Processing with File Uploads

```python
# posts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms

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
    return render(request, 'posts/post_new.html', {'form': form})
```

### Form Template with File Upload

```html
{% extends 'layout.html' %}

{% block content %}
    <h1>New Post</h1>
    <form action="{% url 'posts:new-post' %}" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form }}
        <button type="submit">Add Post</button>
    </form>
{% endblock %}
```

**Key Points:**
- `enctype="multipart/form-data"`: Required for file uploads
- `request.FILES`: Handles uploaded files
- `{% csrf_token %}`: Security protection (required for all POST forms)

### commit=False Pattern

Allows modification before saving:

```python
newpost = form.save(commit=False)  # Create object in memory
newpost.author = request.user       # Set additional fields
newpost.save()                      # Commit to database
```

**Why use commit=False:**
- Set fields not in the form
- Additional processing before saving
- Ensure data integrity
- Required relationship fields

### CSRF Protection

**What it is:**
Cross-Site Request Forgery protection prevents malicious websites from submitting forms.

**How it works:**
1. Django generates unique token for session
2. Token embedded in form as hidden field
3. Django validates token on submission
4. Request processed if valid

**Usage:**
```html
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

### Form Validation

Django automatically validates:
- Field types
- Required fields
- Unique constraints
- Model constraints
- Custom validation methods

**Error handling:**
```python
if form.is_valid():
    # Process form
else:
    # Errors automatically displayed in template
```

---

## Best Practices & Workflows {#best-practices}

### Development Workflow

1. **Plan models** → Define database structure
2. **Create migrations** → `makemigrations` → `migrate`
3. **Create views** → Process requests
4. **Configure URLs** → Route to views
5. **Create templates** → Display data
6. **Test functionality** → Verify features
7. **Iterate** → Refine and improve

### Security Best Practices

- **Always use CSRF tokens** in POST forms
- **Use `@login_required`** for protected views
- **Validate user input** through forms
- **Use POST for state-changing operations** (never GET)
- **Hash passwords** (Django does this automatically)
- **Use ForeignKey relationships** to link data properly
- **Implement proper permissions** for different user roles

### Code Organization

**Models:**
- One model per table
- Use descriptive field names
- Include `__str__()` method
- Add helpful comments

**Views:**
- Keep logic simple
- Use decorators for common functionality
- Return appropriate HTTP responses
- Handle errors gracefully

**Templates:**
- Use inheritance for consistency
- Keep logic minimal
- Use semantic HTML
- Ensure accessibility

**URLs:**
- Use descriptive names
- Organize with app namespaces
- Place specific before general patterns

### Database Best Practices

- **Always create migrations** after model changes
- **Review migrations** before applying
- **Never edit applied migrations**
- **Test on development database** first
- **Keep migrations in version control**
- **Use `order_by()`** for consistent ordering
- **Optimize queries** with `select_related()` and `prefetch_related()`

### Template Best Practices

- **Use template inheritance** for consistency
- **Load static files** with `{% load static %}`
- **Use named URLs** instead of hard-coding
- **Add accessibility attributes** (aria-labels, alt text)
- **Keep templates DRY** (Don't Repeat Yourself)
- **Use semantic HTML5** elements

### Form Best Practices

- **Use ModelForm** when possible
- **Validate on backend** (never trust client-side only)
- **Provide clear error messages**
- **Use appropriate field types**
- **Add help text** for complex fields
- **Test validation thoroughly**

### Common Pitfalls to Avoid

1. **Forgetting to add app to INSTALLED_APPS**
2. **Not running migrations after model changes**
3. **Forgetting CSRF token in forms**
4. **Hard-coding URLs instead of using `{% url %}`**
5. **Not using `commit=False` when setting additional fields**
6. **Forgetting `enctype="multipart/form-data"` for file uploads**
7. **Placing general URL patterns before specific ones**
8. **Not using POST method for logout**

### Django Shell Commands

```python
# Import models
from posts.models import Post
from django.contrib.auth.models import User

# Create objects
p = Post(title="Title", body="Body", slug="slug")
p.save()

# Query
Post.objects.all()
Post.objects.filter(author__username="john")
Post.objects.get(id=1)
Post.objects.order_by('-date')

# Update
p.title = "New Title"
p.save()

# Delete
p.delete()

# Count
Post.objects.count()

# Relationships
user.post_set.all()  # Get all posts by user
```

---

## Complete Feature Checklist

By the end of this guide, you've learned to build a complete Django blog with:

- ✅ Project setup and configuration
- ✅ Multiple Django apps (posts, users)
- ✅ Database models with relationships
- ✅ Migrations workflow
- ✅ Django ORM for database operations
- ✅ Views and URL routing
- ✅ Template inheritance and static files
- ✅ Django admin interface
- ✅ User registration and authentication
- ✅ Login/logout functionality
- ✅ Authorization with decorators
- ✅ Custom forms with ModelForm
- ✅ File uploads (images)
- ✅ CSRF protection
- ✅ Conditional navigation
- ✅ Author attribution for posts

---

## Conclusion

You've now completed a comprehensive Django learning journey, building a fully functional blog application with user authentication, post creation, image uploads, and proper security measures. This foundation prepares you for more advanced Django topics like:

- Class-based views
- REST APIs with Django REST Framework
- Testing and debugging
- Deployment to production
- Performance optimization
- Advanced authentication (OAuth, social auth)
- Real-time features with WebSockets
- Caching strategies

Continue practicing by building additional features and exploring Django's extensive ecosystem. The official Django documentation (docs.djangoproject.com) is an excellent resource for deepening your knowledge.