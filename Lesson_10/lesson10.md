# Django Lesson 10: User Authentication and Login

## Overview
This lesson focuses on implementing user authentication and login functionality using Django's built-in authentication system. We'll add login capabilities, enhance the registration process with automatic login, and improve navigation with login links.

---

## 1. Enhanced Navigation with Login Link

### Changes to `myproject/templates/layout.html`:

**Previous (Lesson 9):**
```html
<nav>
    <a href="/">
        <span rol="img" aria-label="Home">🏠</span>
    </a> |
    <a href="/about">
        <span rol="img" aria-label="About">😊</span>
    </a> |
    <a href="{% url 'posts:list' %}">
        <span rol="img" aria-label="Posts">📰</span>
    </a> |
    <a href="{% url 'users:register' %}">
        <span rol="img" aria-label="User Registration">🚀</span>
    </a> |
</nav>
```

**Updated (Lesson 10):**
```html
<nav>
    <a href="/">
        <span rol="img" aria-label="Home" title="Home">🏠</span> {% comment %} Made the home emoji assigned a role as image {% endcomment %}
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

**Key Changes:**
- **New Login Link**: Added link to user login page using `{% url 'users:login' %}`
- **Enhanced Accessibility**: Added `title` attributes for better tooltip support
- **Lock Icon**: 🔐 emoji represents login/security functionality
- **Consistent Styling**: Maintains same navigation pattern

**Accessibility Improvements:**
- **Title attributes**: Provide hover tooltips for better UX
- **Descriptive labels**: Clear aria-labels for screen readers
- **Semantic navigation**: Proper role assignments for emojis

---

## 2. Enhanced URL Configuration

### Changes to `users/urls.py`:

**Previous (Lesson 9):**
```python
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
]
```

**Updated (Lesson 10):**
```python
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
]
```

**Key Addition:**
- **Login URL pattern**: `path('login/', views.login_view, name='login')`
- **Named URL**: Accessible as `users:login` in templates
- **View mapping**: Routes to new `login_view` function

---

## 3. Enhanced Views with Authentication

### Changes to `users/views.py`:

**Previous (Lesson 9):**
```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts:list")
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {"form": form})
```

**Updated (Lesson 10):**
```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("posts:list")
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {"form": form})

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

**New Imports:**
- **AuthenticationForm**: Django's built-in login form
- **login function**: Django's function to log users in

**Enhanced register_view:**
- **Automatic login**: `login(request, form.save())` logs user in after registration
- **Better UX**: Users don't need to login separately after registering
- **Session creation**: Automatically creates user session

**New login_view:**
- **POST handling**: Processes login form submissions
- **Form validation**: Validates username/password combination
- **User authentication**: `form.get_user()` retrieves authenticated user
- **Session management**: `login(request, user)` creates user session
- **Redirect on success**: Takes user to posts list after login

---

## 4. Django's AuthenticationForm

### Understanding AuthenticationForm:
```python
from django.contrib.auth.forms import AuthenticationForm
```

**Form Features:**
- **Username field**: Text input for username or email
- **Password field**: Password input with proper security
- **Built-in validation**: Checks credentials against database
- **User retrieval**: `get_user()` method returns authenticated user
- **Security features**: Protection against brute force attacks

**Form Data Handling:**
```python
form = AuthenticationForm(data=request.POST)
```
- **Data parameter**: Passes POST data to form
- **Different from ModelForm**: Uses `data=` instead of direct POST
- **Authentication specific**: Designed for login credentials

---

## 5. Django Login Function

### Understanding the login() Function:
```python
from django.contrib.auth import login

login(request, user)
```

**What login() does:**
- **Creates session**: Establishes user session in database
- **Sets cookies**: Sends session cookie to user's browser
- **User tracking**: Enables `request.user` access in views
- **Session management**: Handles session expiration and cleanup

**Login Process:**
1. **Validate credentials**: Check username/password
2. **Get user object**: Retrieve user from database
3. **Create session**: Generate session key
4. **Set cookie**: Send session cookie to browser
5. **Update last_login**: Record when user logged in

---

## 6. Enhanced Registration Flow

### Automatic Login After Registration:
```python
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())  # Auto-login after registration
            return redirect("posts:list")
```

**User Experience Improvement:**
- **Seamless flow**: Register → Automatic login → Redirect to posts
- **Reduced friction**: No need for separate login step
- **Better conversion**: Users immediately access authenticated features

**Technical Process:**
1. **User submits registration**
2. **Form validation passes**
3. **User created in database** (`form.save()`)
4. **User automatically logged in** (`login(request, user)`)
5. **Redirected to posts** (`redirect("posts:list")`)

---

## 7. Login Template Structure

### Expected `templates/users/login.html`:
```html
{% extends 'layout.html' %}

{% block title %}
    User Login
{% endblock %}

{% block content %}
    <h1>Login</h1>
    <form class="form-with-validation" action="/users/login/" method="post">
        {% csrf_token %}
        {{ form }}
        <button class="form-submit">Login</button>
    </form>
{% endblock %}
```

**Template Features:**
- **Similar structure**: Matches registration template pattern
- **CSRF protection**: Required for POST forms
- **Form rendering**: `{{ form }}` displays username/password fields
- **Action URL**: Points to login endpoint

---

## 8. Authentication State Management

### Session Handling:
- **Session creation**: Django creates session on login
- **Session storage**: Session data stored in database
- **Cookie management**: Session ID sent as cookie
- **Session expiration**: Configurable timeout settings

### User Object Access:
```python
# In views, after login
request.user  # Returns logged-in user object
request.user.is_authenticated  # True if user is logged in
request.user.username  # User's username
```

**Template Access:**
```html
<!-- In templates -->
{{ user.username }}  <!-- Display current user -->
{% if user.is_authenticated %}  <!-- Check if logged in -->
    <p>Welcome, {{ user.username }}!</p>
{% endif %}
```

---

## 9. Error Handling and Validation

### Login Form Validation:
- **Invalid credentials**: Wrong username/password combination
- **Non-existent user**: Username not found in database
- **Inactive user**: User account disabled
- **Form errors**: Displayed automatically by Django

### Security Features:
- **Password hashing**: Passwords compared using secure hashing
- **Brute force protection**: Built-in rate limiting
- **Session security**: Secure session cookie settings
- **CSRF protection**: Required token validation

---

## 10. Complete Authentication Flow

### User Registration Flow:
```
Visit /users/register/ → Fill form → Submit → Validate → Create user → Auto-login → Redirect to posts
```

### User Login Flow:
```
Visit /users/login/ → Enter credentials → Submit → Validate → Login → Redirect to posts
```

### Navigation Flow:
```
Home (🏠) → About (😊) → Posts (📰) → Register (🚀) → Login (🔐)
```

---

## Key Concepts Learned

### Authentication System:
- **Built-in forms**: UserCreationForm and AuthenticationForm
- **Login function**: Creating and managing user sessions
- **User objects**: Access to authenticated user information
- **Session management**: Cookie-based session handling

### User Experience:
- **Seamless registration**: Auto-login after registration
- **Consistent navigation**: Clear login/register links
- **Accessibility**: Proper aria-labels and titles
- **Error handling**: Form validation and error display

### Security:
- **CSRF protection**: Required for all POST forms
- **Password security**: Secure hashing and validation
- **Session security**: Proper session management
- **Form validation**: Built-in authentication checks

---

## Next Steps

After implementing authentication and login, you're ready for:
- **User logout functionality**
- **Login required decorators**
- **User profile management**
- **Password change/reset features**
- **Conditional navigation** (show different links for authenticated users)

You now have a complete user authentication system with registration and login capabilities!