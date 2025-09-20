# Django Lesson 9: User Registration Forms

## Overview
This lesson focuses on implementing functional user registration using Django's built-in UserCreationForm. We'll learn about form handling, CSRF protection, form validation, and user authentication. This builds upon the users app structure created in Lesson 8.

---

## 1. Enhanced Base Template Navigation

### Changes to `myproject/templates/layout.html`:

**Previous (Lesson 8):**
```html
<nav>
    <a href="/">🏠</a> |
    <a href="/about">😊</a> |
    <a href="{% url 'posts:list' %}">📰</a> |
</nav>
```

**Updated (Lesson 9):**
```html
<nav>
    <a href="/">
        <span role="img" aria-label="Home">🏠</span> {% comment %} Made the home emoji assigned a role as image {% endcomment %}
    </a> |
    <a href="/about">
        <span role="img" aria-label="About">😊</span>
    </a> |
    <a href="{% url 'posts:list' %}">
        <span role="img" aria-label="Posts">📰</span>
    </a> |
    <a href="{% url 'users:register' %}">
        <span role="img" aria-label="User Registration">🚀</span>
    </a> |
</nav>
```

**Key Changes:**
- **New Registration Link**: Added link to user registration page
- **Accessibility Enhancement**: Added `role="img"` and `aria-label` attributes
- **Semantic HTML**: Better screen reader support for emoji navigation
- **Named URL Reference**: Uses `{% url 'users:register' %}` for registration link

**Accessibility Benefits:**
- **Screen readers**: Can announce what each emoji represents
- **Better UX**: Clearer navigation for users with disabilities
- **Semantic meaning**: Proper role attributes for non-text content

---

## 2. Enhanced Registration View with Form Handling

### Changes to `users/views.py`:

**Previous (Lesson 8):**
```python
from django.shortcuts import render

def register_view(request):
    return render(request, 'users/register.html')
```

**Updated (Lesson 9):**
```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():  # is_valid checks if the user is already available or not
            form.save()
            return redirect("posts:list")
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {"form": form})
```

**New Features Added:**
- **Import redirect**: For redirecting after successful registration
- **Import UserCreationForm**: Django's built-in user registration form
- **POST request handling**: Process form submissions
- **Form validation**: Check if form data is valid
- **User creation**: Save new user to database
- **Redirect after success**: Send user to posts list after registration

**View Logic Flow:**
1. **GET request**: Display empty registration form
2. **POST request**: Process submitted form data
3. **Form validation**: Check username/password requirements
4. **Save user**: Create new user in database
5. **Redirect**: Send to posts page on success
6. **Re-display form**: Show errors if validation fails

---

## 3. Registration Template with Form

### Changes to `templates/users/register.html`:

**Previous (Lesson 8):**
```html
{% extends 'layout.html' %}

{% block title %}
    Register a New User
{% endblock %}

{% block content %}
<h1>Register a New User</h1>
{% endblock %}
```

**Updated (Lesson 9):**
```html
{% extends 'layout.html' %}

{% block title %}
    Register a New User
{% endblock %}

{% block content %}
    <h1>Register a New User</h1>
    <form class="form-with-validation" action="/users/register/" method="post">
        {% csrf_token %} {% comment %} new term learnt {% endcomment %}
        {{ form }}
        <button class="form-submit">Submit</button>
    </form>
{% endblock %}
```

**New Form Elements:**
- **Form tag**: HTML form with POST method
- **Action attribute**: Points to `/users/register/` URL
- **CSRF token**: Security protection against cross-site attacks
- **Form rendering**: `{{ form }}` displays Django form fields
- **Submit button**: Triggers form submission

---

## 4. Understanding CSRF Protection

### What is CSRF Token?
```html
{% csrf_token %} 
```

**CSRF (Cross-Site Request Forgery) Protection:**
- **Security measure**: Prevents malicious websites from submitting forms
- **Token generation**: Django creates unique token for each form
- **Validation**: Django checks token on form submission
- **Required for POST**: All POST forms need CSRF token

**How it works:**
1. **Django generates** unique token for user session
2. **Token embedded** in form as hidden field
3. **User submits** form with token
4. **Django validates** token matches session
5. **Request processed** if token is valid

**Security Benefits:**
- **Prevents attacks**: Malicious sites can't forge requests
- **Session validation**: Ensures request comes from legitimate user
- **Automatic protection**: Django handles token generation/validation

---

## 5. Django's UserCreationForm

### Built-in Form Features:
```python
from django.contrib.auth.forms import UserCreationForm
```

**UserCreationForm provides:**
- **Username field**: Text input for unique username
- **Password1 field**: Password input with validation
- **Password2 field**: Password confirmation field
- **Built-in validation**: Checks password strength and username availability
- **User model integration**: Automatically works with Django's User model

**Form Validation Rules:**
- **Username uniqueness**: Prevents duplicate usernames
- **Password strength**: Enforces minimum password requirements
- **Password matching**: Ensures password and confirmation match
- **Field requirements**: Validates required fields are filled

---

## 6. Form Validation Process

### View Validation Logic:
```python
if form.is_valid():  # is_valid checks if the user is already available or not
    form.save()
    return redirect("posts:list")
```

**Validation Steps:**
1. **Field validation**: Check individual field requirements
2. **Username check**: Verify username doesn't already exist
3. **Password validation**: Ensure password meets Django's requirements
4. **Cross-field validation**: Confirm passwords match
5. **Custom validation**: Any additional form validation rules

**Validation Outcomes:**
- **Valid form**: User created and redirected to posts
- **Invalid form**: Form re-displayed with error messages
- **Error display**: Django automatically shows validation errors

---

## 7. HTTP Request Methods

### GET vs POST Handling:
```python
if request.method == 'POST':
    # Process form submission
    form = UserCreationForm(request.POST)
else:
    # Display empty form
    form = UserCreationForm()
```

**Request Method Logic:**
- **GET request**: User navigates to registration page
- **POST request**: User submits registration form
- **Method checking**: Different logic for different HTTP methods
- **Form initialization**: Empty form for GET, populated for POST

---

## 8. User Registration Flow

### Complete Registration Process:

1. **User clicks registration link** → GET `/users/register/`
2. **Django displays form** → Empty UserCreationForm
3. **User fills form** → Username and passwords
4. **User submits form** → POST `/users/register/`
5. **Django validates** → Check username/password requirements
6. **If valid** → Save user and redirect to posts
7. **If invalid** → Re-display form with errors

```
Navigation → Form Display → User Input → Form Submission → Validation → Success/Error
```

---

## 9. Django Authentication System Integration

### Built-in User Model:
- **Username field**: Unique identifier for users
- **Password field**: Hashed and stored securely
- **Email field**: Optional email address
- **Date fields**: When user was created/last logged in
- **Permission fields**: User groups and permissions

**Database Integration:**
- **User creation**: Automatically saved to auth_user table
- **Password hashing**: Django handles secure password storage
- **User management**: Ready for authentication features

---

## 10. Error Handling and User Feedback

### Form Error Display:
```html
{{ form }}  <!-- Automatically includes error messages -->
```

**Error Types:**
- **Field errors**: Username taken, password too weak
- **Form errors**: Passwords don't match
- **Required field errors**: Empty required fields
- **Custom validation errors**: Any additional validation rules

**User Experience:**
- **Inline errors**: Displayed next to relevant fields
- **Clear messages**: Descriptive error messages
- **Form persistence**: User input preserved on errors
- **Accessibility**: Error messages properly associated with fields

---

## Key Concepts Learned

### Form Handling:
- **Django forms**: Built-in form classes and validation
- **Request methods**: Different handling for GET vs POST
- **Form processing**: Validation, saving, and error handling
- **User feedback**: Success redirects and error display

### Security:
- **CSRF protection**: Preventing cross-site request forgery
- **Password security**: Django's built-in password validation
- **User validation**: Preventing duplicate usernames

### Accessibility:
- **Semantic HTML**: Proper role and aria-label attributes
- **Screen reader support**: Better navigation for disabled users
- **Form accessibility**: Proper error message association

---

## Next Steps

After completing user registration, you're ready for:
- **User login/logout functionality**
- **User authentication decorators**
- **User profile management**
- **Password reset functionality**
- **User permissions and groups**

You now have a functional user registration system integrated with Django's authentication framework!