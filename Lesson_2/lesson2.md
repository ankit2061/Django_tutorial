# Django Lesson 2: Creating Apps and Templates

## Overview
This lesson covers the fundamental steps to create a Django app, set up templates, views, and URL routing.

---

## 1. Creating a Django App

### Command
```bash
python manage.py startapp posts
```

**What this does:**
- Creates a new Django app named `posts`
- Generates the basic app structure with necessary files

---

## 2. Setting Up Templates

### Template Directory Structure
Based on your project structure, the templates are inside the `posts` app:

```
posts/
└── templates/
    └── posts/
        └── posts_list.html
```

**Steps:**
1. Inside the `posts` app directory, there's already a `templates` folder
2. Inside `templates`, create a directory named `posts` (same as the app name)
3. Create the HTML file `posts_list.html` inside the `posts` directory

> **Note:** Templates are organized within each app's directory, not at the project root level.

---

## 3. Creating Views

### File: `posts/views.py`

```python
from django.shortcuts import render

def posts_list(request):
    return render(request, 'posts/posts_list.html')
```

**Key Points:**
- Import the `render` function from `django.shortcuts`
- Create a view function that takes `request` as parameter
- Use `render()` to return the HTML template

---

## 4. URL Configuration

### File: `posts/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts_list, name='posts_list'),
]
```

**Important:**
- Use empty string `''` for the path since we're already in the posts URL namespace
- This avoids redundant `/posts/posts` in the URL structure

---

## 5. Registering the App

### File: `myproject/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'posts',  # Add your app here
]
```

**Critical Step:**
- Always add your new app to `INSTALLED_APPS`
- Without this, Django won't recognize your app

---

## 6. Main Project URL Configuration

### File: `myproject/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
]
```

**Note:** Don't forget to include your app's URLs in the main project URLs!

---

## Summary Checklist

- [ ] Create app with `python manage.py startapp posts`
- [ ] Set up template directory structure
- [ ] Create view function in `views.py`
- [ ] Configure URLs in `posts/urls.py`
- [ ] Add app to `INSTALLED_APPS` in `settings.py`
- [ ] Include app URLs in main project `urls.py`

---

## File Structure Overview

Based on the actual project structure:

```
Lesson_2/
├── myproject/
│   ├── myproject/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── posts/
│   │   ├── __pycache__/
│   │   ├── migrations/
│   │   ├── templates/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── static # same as lesson_1
│   │   ├── css
│   │   │   └── style.css
│   │   └── js
│   │   │   └── main.js
│   ├── templates # same as lesson_1
│   │   ├── about.html
│   │   └── home.html
│   ├── db.sqlite3
│   └── manage.py
└── lesson2.md
```