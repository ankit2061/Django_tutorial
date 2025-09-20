# Django Lesson 6: Pages, URLs & Slugs

## Overview
This lesson covers URL routing, slugs for SEO-friendly URLs, path converters, and creating individual post pages. We'll learn how to link between pages and organize URL patterns using app namespaces.

---

## 1. Enhanced Base Template

### Changes to `layout.html` (from Lesson 5):

**Previous (Lesson 5):**
```html
<nav>
    <a href="/">🏠</a> |
    <a href="/about">😊</a> |
    <a href="/posts">📰</a> |
</nav>
```

**Updated (Lesson 6):**
```html
<nav>
    <a href="/">🏠</a> |
    <a href="/about">😊</a> |
    <a href="{% url 'posts:list' %}">📰</a> |
</nav>
```

**Key Change:**
- **Hard-coded URL replaced**: Changed from `/posts` to `{% url 'posts:list' %}`
- **Named URL with namespace**: Uses Django's URL reversing system
- **Better maintainability**: URL changes automatically update throughout templates

**Why This Change Matters:**
- **DRY Principle**: Don't repeat URL patterns in multiple places
- **Flexibility**: Can change URL structure without updating every template
- **App Namespace**: `posts:list` clearly identifies which app's URL we're using

---

## 2. URL Configuration with App Namespace

### In `posts/urls.py`:
```python
from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.posts_list, name="list"),  # We are already in posts path so we are writing '' instead of '/posts'
    path('<slug:slug>', views.posts_page, name="page"),  # Using path converter
]
```

**Key Concepts:**
- **app_name**: Creates namespace 'posts' for URL reversing
- **Empty path**: `''` matches the base posts URL
- **Path Converter**: `<slug:slug>` captures slug from URL
- **Named URLs**: `name="list"` and `name="page"` for template references

**Path Converter Types:**
- `<slug:slug>`: Matches slug patterns (letters, numbers, hyphens, underscores)
- `<int:id>`: Matches integers
- `<str:name>`: Matches strings
- `<path:path>`: Matches paths including forward slashes

---

## 3. Updated Views with Slug Support

### In `posts/views.py`:
```python
from django.shortcuts import render
from .models import Post  # new import

# Create your views here.
def posts_list(request):
    posts = Post.objects.all().order_by('-date')  # referred from previous ORM lecture and added order_by constraint
    return render(request, 'posts/posts_list.html', {'posts': posts})  # we added extra parameter of dictionary here

def posts_page(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'posts/post_page.html', {'post': post})  # we added extra parameter of dictionary here
```

**Code Explanation:**
```python
'''
So what are we basically doing here?
We are bringing in 'Post' model ->
we are getting all of the posts ->
passing all of that data on to the template
'''
```

**New View Function - `posts_page`:**
- **Parameter**: `slug` captured from URL
- **Database Query**: `Post.objects.get(slug=slug)` finds specific post
- **Single Object**: Returns one post instead of all posts
- **Template Rendering**: Uses `post_page.html` template

---

## 4. Enhanced Posts List Template

### Changes to `templates/posts/posts_list.html`:

**Previous (Lesson 5):**
```html
<article class="post">
    <h2>{{ post.title }}</h2>
    <p>{{ post.date }}</p>
    <p>{{ post.body }}</p>
</article>
```

**Updated (Lesson 6):**
```html
<article class="post">
    <h2>
        <a href="{% url 'posts:page' slug=post.slug %}">
            {% comment %} we have added the 'posts:' to emphasize that the page is from posts app only, this would become helpful when we are making large projects {% endcomment %}
            {{ post.title }}
        </a>
    </h2>
    <p>{{ post.date }}</p>
    <p>{{ post.body }}</p>
</article>
```

**Key Changes:**
- **Clickable Titles**: Post titles now wrapped in `<a>` tags
- **Named URL with Namespace**: `{% url 'posts:page' slug=post.slug %}`
- **Slug Parameter**: Passes each post's slug to generate individual URLs
- **App Namespace Benefits**: `posts:` prefix prevents URL name conflicts in large projects

---

## 5. NEW: Individual Post Page Template

### Created `templates/posts/post_page.html`:
```html
{% extends 'layout.html' %}

{% block title %}
    {{ post.title }}
{% endblock %}

{% block content %}
<section>
    <h1>{{ post.title }}</h1>
    <p>{{ post.date }}</p>
    <p>{{ post.body }}</p>
</section>
{% endblock %}
```

**Template Features:**
- **NEW FILE**: This template didn't exist in Lesson 5
- **Dynamic Title**: Page title shows the individual post title
- **Clean Layout**: Simple presentation of single post content
- **Consistent Design**: Extends same base layout as posts list
- **Single Post Display**: Shows one post's complete information

---

## 6. NEW: URL Configuration with App Namespace

### Created `posts/urls.py`:
```python
from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.posts_list, name="list"),  # We are already in posts path so we are writing '' instead of '/posts'
    path('<slug:slug>', views.posts_page, name="page"),  # Using path converter
]
```

**NEW Concepts:**
- **app_name**: Creates namespace 'posts' for URL reversing (NEW)
- **Path Converter**: `<slug:slug>` captures slug from URL (NEW)
- **Slug-based URLs**: Individual posts accessible via their slug (NEW)
- **Named URLs**: Both views now have names for template reference

### Complete URL Structure:
```
Main Project URLs → App URLs → View Functions
/posts/           → ''       → posts_list
/posts/my-slug/   → '<slug:slug>' → posts_page
```

**URL Resolution Process:**
1. **Django matches** `/posts/` in main urls.py
2. **Forwards to** posts app urls.py
3. **Matches pattern** in app's urlpatterns
4. **Calls view function** with captured parameters

---

## 9. Template URL Reversing

### Named URL Benefits:
```html
<!-- Hard-coded URL (bad) -->
<a href="/posts/my-first-post/">My First Post</a>

<!-- Named URL (good) -->
<a href="{% url 'posts:page' slug=post.slug %}">{{ post.title }}</a>
```

**Advantages:**
- **Flexibility**: Change URL patterns without updating templates
- **Maintainability**: Single source of truth for URL structure
- **Error Prevention**: Django validates URL names at runtime

---

## Key Concepts Learned

### URL Patterns:
- **App namespaces** prevent URL name conflicts
- **Path converters** capture URL segments as view parameters
- **Named URLs** enable flexible template linking

### Django MVT Pattern:
- **Model**: Post model defines data structure
- **View**: Functions process requests and query database
- **Template**: HTML with Django tags renders final output

### Database Integration:
- **Admin interface** provides easy content management
- **ORM queries** connect database to views
- **Template variables** display dynamic content

---

## Next Steps

After completing this lesson, you're ready to explore:
- **URL parameters and filtering**
- **Form handling for user input**
- **Static files organization**
- **CSS styling for better presentation**
- **Error handling for missing posts**

You now have a complete blog system with admin management and public viewing pages!