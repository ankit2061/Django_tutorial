# Django Blog - Complete Learning Journey

A comprehensive Django blog application built from scratch, documenting the complete learning journey from basic setup to advanced features like user authentication, authorization, and file uploads.

## 📚 Project Overview

This repository contains a fully functional blog application built with Django, featuring user authentication, post creation with image uploads, and a complete admin interface. The project serves as a practical learning resource for Django fundamentals.

## ✨ Features

- **User Management**
  - User registration with automatic login
  - Login/logout functionality
  - Session management
  - Password validation and security

- **Blog Posts**
  - Create, read, and display blog posts
  - Rich text content with titles and body
  - SEO-friendly slugs for URLs
  - Image banner uploads
  - Author attribution
  - Automatic date/time tracking

- **Authorization & Security**
  - Login-required decorators for protected views
  - CSRF protection on all forms
  - Conditional navigation based on authentication
  - Secure file upload handling

- **Admin Interface**
  - Django admin for content management
  - Model registration
  - Easy post creation and editing

## 🛠️ Tech Stack

- **Framework:** Django 5.2
- **Database:** SQLite (development)
- **Python:** 3.12+
- **Image Processing:** Pillow
- **Frontend:** HTML5, CSS3, JavaScript (vanilla)

## 📁 Project Structure

```
myproject/
├── myproject/              # Project configuration
│   ├── settings.py        # Main settings
│   ├── urls.py            # Root URL configuration
│   └── views.py           # Project-level views
├── posts/                 # Blog posts app
│   ├── migrations/        # Database migrations
│   ├── templates/         # App templates
│   ├── admin.py          # Admin configuration
│   ├── forms.py          # Custom forms
│   ├── models.py         # Post model
│   ├── urls.py           # App URL patterns
│   └── views.py          # Post views
├── users/                # User authentication app
│   ├── templates/        # User templates
│   ├── urls.py          # Auth URL patterns
│   └── views.py         # Auth views
├── templates/            # Project-level templates
│   ├── layout.html      # Base template
│   ├── home.html
│   └── about.html
├── static/              # Static files
│   ├── css/
│   └── js/
├── media/               # User uploads
├── db.sqlite3          # Database
└── manage.py           # Django CLI
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/django-blog.git
   cd django-blog
   ```

2. **Create and activate virtual environment**
   ```bash
   # On macOS/Linux
   python -m venv env_site
   source env_site/bin/activate

   # On Windows
   python -m venv env_site
   env_site\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django pillow
   ```

4. **Apply migrations**
   ```bash
   cd myproject
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: `http://127.0.0.1:8000/`
   - Admin interface: `http://127.0.0.1:8000/admin/`
   - Posts: `http://127.0.0.1:8000/posts/`

## 📖 Learning Path

This project was built through a structured 12-lesson learning journey:

1. **Lesson 1-2:** Project setup, apps, and templates
2. **Lesson 3:** Models and migrations
3. **Lesson 4:** Django ORM basics
4. **Lesson 5:** Django admin interface
5. **Lesson 6:** URLs, slugs, and page routing
6. **Lesson 7:** Image uploads and media files
7. **Lesson 8:** Creating the users app (Challenge)
8. **Lesson 9:** User registration forms
9. **Lesson 10:** User authentication and login
10. **Lesson 11:** Authorization and access control
11. **Lesson 12:** Custom forms and post creation

Detailed lesson notes are available in the `lesson*.md` files.

## 🔑 Key Concepts Covered

### Models & Database
- Model field types and parameters
- ForeignKey relationships
- Database migrations workflow
- Django ORM queries

### Views & URLs
- Function-based views
- URL routing and namespacing
- Path converters
- Request/response handling

### Templates
- Template inheritance
- Template tags and filters
- Static files integration
- Conditional rendering

### Forms
- ModelForm creation
- Form validation
- File upload handling
- CSRF protection

### Authentication
- User registration
- Login/logout functionality
- Session management
- Login-required decorators

### Authorization
- Access control with decorators
- Conditional navigation
- User permissions
- "Next" parameter handling

## 📝 Usage Examples

### Creating a New Post

1. Log in to the application
2. Click the "New Post" link (🆕)
3. Fill in the form:
   - Title
   - Body content
   - Slug (URL-friendly)
   - Banner image (optional)
4. Submit the form

### User Registration

1. Navigate to registration page (🚀)
2. Enter username and password
3. Confirm password
4. Automatic login after successful registration

### Admin Management

1. Access `/admin/`
2. Log in with superuser credentials
3. Manage posts, users, and other content

## 🔒 Security Features

- CSRF protection on all forms
- Password hashing and validation
- Login-required decorators for protected views
- Secure session management
- File upload validation
- SQL injection protection (Django ORM)

## 🎨 Customization

### Adding New Fields to Post Model

```python
# posts/models.py
class Post(models.Model):
    # ... existing fields
    excerpt = models.TextField(max_length=200, blank=True)
    
    def __str__(self):
        return self.title
```

Then run:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Customizing Templates

Edit templates in `templates/` or `app/templates/` directories. The base template `layout.html` controls the overall site structure.

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)

## 🤝 Contributing

This is a learning project, but suggestions and improvements are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Ankit Talukder**

- GitHub: [@ankit2061](https://github.com/ankit2061)

## 🙏 Acknowledgments

- Django Software Foundation
- https://youtu.be/Rp5vd34d-z4?si=Nu7dJxKsEoQ0MsL8
- Python community
- All contributors to Django documentation

## 📞 Support

If you have questions or need help:

1. Check the lesson notes (lesson*.md files)
2. Review Django documentation
3. Open an issue on GitHub

---

**Note:** This is a learning project for educational purposes. For production deployment, additional security measures and configurations are recommended.