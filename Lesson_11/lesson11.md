# Django Lesson 11: User Authorization and Access Control

## Overview
This lesson focuses on user authorization, which controls what authenticated users can do. We'll implement logout functionality, conditional navigation based on authentication status, login-required decorators, and "next" parameter handling for better user experience.

---

## 1. Conditional Navigation Based on Authentication

### Major Changes to `myproject/templates/layout.html`:

**Previous (Lesson 10):**
```html
<nav>
    <a href="/">
        <span rol="img" aria-label="Home" title="Home">🏠</span>
    </a> |
    <a href="/about">
        <span rol="img" aria-label="About" title="About">😊</span>
    </a> |
    <a href="{% url 'posts:list' %}">
        <span rol="img" aria-label="Posts" title="Posts">📰</span>
    </a> | 
    <a href="{% url 'users:register' %}">
        <span rol="img" aria-label="User Registration" title="User Registration">🚀</span>
    </a> |
    <a href="{% url 'users:login' %}">
        <span rol="img" aria-label="User Login" title="User Login">🔐</span>
    </a> 
</nav>
```

**Updated (Lesson 11):**
```html
<nav>
    <a href="/">
        <span rol="img" aria-label="Home" title="Home">🏠</span>
    </a> |
    <a href="/about">
        <span rol="img" aria-label="About" title="About">😊</span>
    </a> |
    <a href="{% url 'posts:list' %}">
        <span rol="img" aria-label="Posts" title="Posts">📰</span>
    </a> | 
    
    {% if user.is_authenticated %}
        <a href="{% url 'posts:new_post' %}">
            <span rol="img" aria-label="New Post" title="New Post">🆕</span>
        </a> |
        <form class="logout" action="{% url 'users:logout' %}" method="post">
            {% csrf_token %}
            <button class="logout-button" aria-label="User Logout" title="User Logout">👋</button>
        </form>
    
    {% else %}
        <a href="{% url 'users:register' %}">
            <span rol="img" aria-label="User Registration" title="User Registration">🚀</span>
        </a> |
        <a href="{% url 'users:login' %}">
            <span rol="img" aria-label="User Login" title="User Login">🔐</span>
        </a> |
    {% endif %}
</nav>
```

**Key Authorization Features:**
- **Conditional Display**: `{% if user.is_authenticated %}` shows different content based on login status
- **Authenticated Users See**: New Post link (🆕) and Logout button (👋)
- **Non-authenticated Users See**: Register (🚀) and Login (🔐) links
- **Logout Form**: POST form with CSRF protection for secure logout
- **Better UX**: Users only see relevant navigation options

---

## 2. Logout Functionality

### Enhanced `users/urls.py`:

**Previous (Lesson 10):**
```python
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
]
```

**Updated (Lesson 11):**
```python
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
```

**New Addition:**
- **Logout URL**: `path('logout/', views.logout_view, name='logout')`
- **Named URL**: Accessible as `users:logout` in templates

---

## 3. Enhanced Views with Logout and "Next" Parameter

### Changes to `users/views.py`:

**Previous (Lesson 10):**
```python
from django.contrib.auth import login

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("posts:list")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {"form": form})
```

**Updated (Lesson 11):**
```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, logout

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

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("posts:list")
```

**New Features:**

### Logout Import and Function:
- **Import logout**: `from django.contrib.auth import login, logout`
- **logout_view**: New function to handle user logout
- **POST only**: Logout only accepts POST requests for security
- **Session cleanup**: `logout(request)` clears user session
- **Redirect**: Takes user to posts list after logout

### "Next" Parameter Handling:
- **Smart redirects**: `if "next" in request.POST:`
- **Return to origin**: Redirects user to page they came from
- **Fallback**: Goes to posts list if no "next" parameter
- **Better UX**: Users return to where they were before login

---

## 4. Login Required Decorator

### Enhanced `posts/views.py`:

**Previous (Lessons 6-10):**
```python
from django.shortcuts import render
from .models import Post

def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'posts/posts_list.html', {'posts': posts})

def posts_page(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'posts/post_page.html', {'post': post})
```

**Updated (Lesson 11):**
```python
from django.shortcuts import render
from .models import Post 
from django.contrib.auth.decorators import login_required  # new import

def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'posts/posts_list.html', {'posts': posts})

def posts_page(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'posts/post_page.html', {'post': post})

@login_required(login_url="/users/login/")
def posts_new(request):
    return render(request, 'posts/post_new.html')
```

**Authorization Features:**
- **New Import**: `from django.contrib.auth.decorators import login_required`
- **New View**: `posts_new` for creating new posts
- **Decorator Protection**: `@login_required(login_url="/users/login/")`
- **Access Control**: Only authenticated users can access new post creation

### How @login_required Works:
1. **User accesses protected view** → `/posts/new-post/`
2. **Django checks authentication** → `request.user.is_authenticated`
3. **If authenticated** → View executes normally
4. **If not authenticated** → Redirects to login page
5. **After login** → Returns to original page using "next" parameter

---

## 5. New Post URL Configuration

### Enhanced `posts/urls.py`:

**Previous (Lesson 6):**
```python
urlpatterns = [
    path('', views.posts_list, name="list"),
    path('<slug:slug>', views.posts_page, name="page"),
]
```

**Updated (Lesson 11):**
```python
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.posts_list, name="list"),
    path('new-post/', views.posts_new, name="new_post"),
    path('<slug:slug>', views.posts_page, name="page"),
]
```

**Important URL Order:**
- **Specific before general**: `new-post/` comes before `<slug:slug>`
- **URL precedence**: Django matches URLs in order
- **Conflict prevention**: Prevents `new-post` from being treated as a slug

---

## 6. Project-Level Template Integration

### Enhanced `myproject/views.py`:

**Previous (implied from earlier lessons):**
```python
from django.http import HttpResponse

def Homepage(request):
    return HttpResponse("Hello World! This is my homepage")

def about(request):
    return HttpResponse("My About Page.")
```

**Updated (Lesson 11):**
```python
from django.shortcuts import render

def Homepage(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')
```

**Template Integration:**
- **Removed HttpResponse**: No longer returning plain text
- **Template rendering**: Using proper HTML templates
- **Consistent design**: Home and About pages use layout.html

### New Template Files:

**`templates/home.html`:**
```html
{% extends 'layout.html' %}

{% block title %}
    Home
{% endblock %}

{% block content %}
    <h1>Home</h1>
    <p>Check out my <a href="/about">About</a> Page</p>
{% endblock %}
```

**`templates/about.html`:**
```html
{% extends 'layout.html' %}

{% block title %}
    About
{% endblock %}

{% block content %}
    <h1>About</h1>
    <p>Check out my <a href="/about">Home</a> Page</p>
{% endblock %}
```

---

## 7. Authentication vs Authorization

### Key Differences:

**Authentication (Who you are):**
- **Login process**: Verifying user credentials
- **Session creation**: Establishing user identity
- **User object**: `request.user` contains user information

**Authorization (What you can do):**
- **Access control**: Determining what authenticated users can access
- **Permission checking**: `@login_required` decorator
- **Conditional content**: Different navigation for different users

### Django's Authorization Tools:

**Template-level Authorization:**
```html
{% if user.is_authenticated %}
    <!-- Content for logged-in users -->
{% else %}
    <!-- Content for anonymous users -->
{% endif %}
```

**View-level Authorization:**
```python
@login_required(login_url="/users/login/")
def protected_view(request):
    # Only authenticated users can access this
    pass
```

---

## 8. Security Considerations

### CSRF Protection:
```html
<form class="logout" action="{% url 'users:logout' %}" method="post">
    {% csrf_token %}
    <button class="logout-button">👋</button>
</form>
```

**Why POST for Logout:**
- **CSRF protection**: GET requests are vulnerable to CSRF attacks
- **Security best practice**: State-changing operations should use POST
- **Token validation**: Django validates CSRF token on submission

### Login URL Security:
```python
@login_required(login_url="/users/login/")
```
- **Explicit login URL**: Specifies where to redirect unauthorized users
- **Prevents errors**: Avoids Django's default login URL assumptions
- **Customizable**: Can point to any login page

---

## 9. User Experience Improvements

### Smart Navigation:
- **Context-aware**: Shows relevant options based on user state
- **Reduced clutter**: Only displays applicable links
- **Intuitive icons**: Clear visual indicators for each action

### Redirect Flow:
```
User tries to access /posts/new-post/ → 
Not authenticated → 
Redirected to /users/login/?next=/posts/new-post/ → 
User logs in → 
Redirected back to /posts/new-post/
```

### Logout Flow:
```
User clicks logout button → 
POST to /users/logout/ → 
Session cleared → 
Redirected to posts list → 
Navigation updates to show login/register
```

---

## Key Concepts Learned

### Authorization Techniques:
- **Conditional templates**: `{% if user.is_authenticated %}`
- **View decorators**: `@login_required`
- **URL redirection**: "next" parameter handling
- **Secure logout**: POST-only logout with CSRF protection

### User Experience:
- **Context-aware navigation**: Different options for different users
- **Smart redirects**: Return users to their intended destination
- **Seamless flow**: Smooth authentication and authorization experience

### Security:
- **Access control**: Protecting views from unauthorized access
- **CSRF protection**: Secure form submissions
- **Session management**: Proper login/logout handling

---

## Next Steps

After implementing authorization, you're ready for:
- **User permissions and groups**
- **Object-level permissions**
- **Role-based access control**
- **Custom decorators**
- **Advanced authorization patterns**

You now have a complete authentication and authorization system with proper access control and user experience considerations!