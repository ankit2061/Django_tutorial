# Django Lesson 7: Uploading Images

## Overview
This lesson covers image handling in Django, including installing Pillow, configuring media files, adding ImageField to models, and displaying images in templates. We'll learn how Django manages file uploads and serves media files during development.

---

## 1. Installing Pillow

### Command
```bash
pip install Pillow
```

**What is Pillow:**
- **Python Imaging Library**: Required for Django's ImageField
- **Image Processing**: Handles image validation and manipulation
- **File Format Support**: Supports JPEG, PNG, GIF, and other formats
- **Django Requirement**: Mandatory for using ImageField in models

**Why Pillow is Needed:**
- Validates uploaded image files
- Provides image processing capabilities
- Handles different image formats automatically
- Integrates seamlessly with Django's file handling

---

## 2. Adding ImageField to Post Model

### Changes to `models.py`:
```python
# Previous model (from Lesson 6)
class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)

# NEW in Lesson 7
class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(default='fallback.png', blank=True)  # added blank=True
```

**ImageField Parameters:**
- **default='fallback.png'**: Default image when no image is uploaded
- **blank=True**: Allows empty values in forms (optional field)
- **ImageField**: Specialized FileField for handling images

**Key Points:**
- **File Storage**: Images stored in MEDIA_ROOT directory
- **Validation**: Automatically validates image formats
- **Optional Field**: blank=True makes it optional in admin forms
- **Fallback Image**: Default image shown when none uploaded

---

## 3. Database Migration for ImageField

### Commands and Output:
```bash
python manage.py makemigrations
```

**Terminal Output:**
```bash
(env_site) (base) ankittalukder@Ankits-MacBook-Air myproject % python manage.py makemigrations
Migrations for 'posts':
  posts/migrations/0002_post_banner.py
    + Add field banner to post
```

```bash
python manage.py migrate
```

**Terminal Output:**
```bash
(env_site) (base) ankittalukder@Ankits-MacBook-Air myproject % python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, posts, sessions
Running migrations:
  Applying posts.0002_post_banner... OK
```

**What Happened:**
- **New Migration**: Created `0002_post_banner.py` migration file
- **Database Update**: Added `banner` column to posts table
- **Field Addition**: Existing posts get default fallback image
- **Schema Change**: Database structure updated for image storage

---

## 4. Media Files Configuration

### Changes to `settings.py`:
```python
# NEW in Lesson 7 - Add at the end of settings.py
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

**Configuration Explanation:**
- **MEDIA_URL**: URL prefix for accessing media files (`/media/`)
- **MEDIA_ROOT**: Filesystem path where uploaded files are stored
- **BASE_DIR**: Project root directory
- **Directory Creation**: Django creates `media/` folder automatically

**File Storage Structure:**
```
myproject/
├── media/
│   ├── fallback.png
│   └── uploaded_images/
├── static/
└── templates/
```

---

## 5. URL Configuration for Media Files

### Changes to main `urls.py`:
```python
# Previous imports
from django.contrib import admin
from django.urls import path, include

# NEW imports in Lesson 7
from django.conf.urls.static import static  # new import
from django.conf import settings  # new import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
]

# NEW line added in Lesson 7
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**What This Does:**
- **Development Server**: Enables media file serving during development
- **URL Pattern**: Maps `/media/filename.jpg` to actual file location
- **Static Serving**: Uses Django's static file serving for media files
- **Production Note**: This setup is only for development, not production

**URL Mapping Example:**
```
URL: /media/my-banner.jpg
→ File: myproject/media/my-banner.jpg
```

---

## 6. Automatic Media Directory Creation

### Directory Structure:
```
myproject/
├── media/           # Created automatically
│   └── fallback.png # Default image file
├── posts/
├── templates/
└── static/
```

**Automatic Creation:**
- **Media folder**: Created when first image is uploaded via Django admin
- **Subdirectories**: Django creates subdirectories as needed
- **File Organization**: Images organized by upload date or custom logic
- **Permissions**: Proper file permissions set automatically

---

## 7. Displaying Images in Templates

### Changes to `post_page.html`:
```html
{% extends 'layout.html' %}

{% block title %}
    {{ post.title }}
{% endblock %}

{% block content %}
<section>
    <!-- NEW: Image display -->
    <img src="{{ post.banner.url }}" alt="{{ post.title }}" />
    
    <h1>{{ post.title }}</h1>
    <p>{{ post.date }}</p>
    <p>{{ post.body }}</p>
</section>
{% endblock %}
```

**Image Tag Elements:**
- **src="{{ post.banner.url }}"**: Gets the full URL to the image file
- **alt="{{ post.title }}"**: Accessibility attribute using post title
- **Image URL**: Automatically resolves to `/media/filename.jpg`

**URL Generation:**
- **post.banner.url**: Returns full URL path to image
- **Automatic Resolution**: Django handles URL construction
- **Fallback Handling**: Shows default image if none uploaded

---

## 8. Django Admin Image Management

### Admin Interface Features:
- **File Upload**: Browse and select image files
- **Image Preview**: Shows thumbnail of uploaded images
- **File Validation**: Automatically validates image formats
- **Default Handling**: Uses fallback.png when no image selected

**Admin Workflow:**
1. **Login to admin**: Access `/admin/` interface
2. **Edit Post**: Click on any post to edit
3. **Upload Image**: Use file browser to select image
4. **Save Post**: Image automatically uploaded to media directory
5. **View Result**: Image appears on post page

---

## 9. File Handling Best Practices

### Image Storage:
- **Organized Structure**: Django can organize uploads by date
- **File Naming**: Django handles filename conflicts automatically
- **Size Validation**: Can add file size limits if needed
- **Format Validation**: ImageField validates image formats

### Security Considerations:
- **File Type Validation**: Only allows valid image files
- **Upload Location**: Files stored outside web root for security
- **File Size**: Consider adding upload_to and file size limits

**Example with upload_to:**
```python
banner = models.ImageField(
    default='fallback.png',
    blank=True,
    upload_to='post_banners/'  # Organizes files in subdirectory
)
```

---

## 10. Development vs Production

### Development Setup (Current):
- **Django serves media**: Using `static()` function
- **Local file system**: Files stored locally
- **Simple configuration**: Works out of the box

### Production Considerations:
- **Web server serves media**: Nginx/Apache handles media files
- **Cloud storage**: AWS S3, Google Cloud Storage
- **CDN integration**: Content delivery networks for performance

---

## Key Concepts Learned

### ImageField Features:
- **File Upload**: Handles image file uploads automatically
- **Validation**: Ensures uploaded files are valid images
- **URL Generation**: Provides convenient access to file URLs
- **Integration**: Works seamlessly with Django admin

### Media File Management:
- **Configuration**: MEDIA_URL and MEDIA_ROOT settings
- **Serving**: Development server configuration for media files
- **Organization**: Automatic directory creation and file management

### Template Integration:
- **Image Display**: Using `{{ post.banner.url }}` in templates
- **Accessibility**: Proper alt attributes for images
- **Responsive Design**: Images can be styled with CSS

---

## Next Steps

After completing this lesson, you can explore:
- **Image resizing and thumbnails**
- **Multiple image uploads per post**
- **Image cropping and editing**
- **Cloud storage integration**
- **Advanced file validation**

You now have a complete blog system with image upload capabilities!