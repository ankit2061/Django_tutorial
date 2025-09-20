# Django Lesson 3: Models and Migrations

## Overview
This lesson covers the fundamentals of Django Models and the migration system. Models define your database structure, while migrations handle database schema changes automatically.

---

## 1. Creating Your First Model

### In models.py (inside posts app)

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
```

**What this does:**
- Creates a new class named `Post` that inherits from `models.Model`
- **title**: CharField with maximum 200 characters for post titles
- **body**: TextField for unlimited text content (post content)
- **slug**: SlugField for URL-friendly versions of titles
- **date**: DateTimeField that automatically sets creation timestamp
- **__str__()**: Returns a human-readable representation of the model

**Key Model Field Types:**
- `CharField`: Short text with character limit
- `TextField`: Long text without character limit
- `SlugField`: URL-friendly text (lowercase, hyphens instead of spaces)
- `DateTimeField`: Date and time information

---

## 2. Initial Database Migration

### Command
```bash
python manage.py migrate
```

**What this does:**
1. Applies Django's built-in migrations (auth, admin, contenttypes, sessions)
2. Creates the initial database tables for Django's core functionality
3. Sets up the database structure before adding custom models

**Steps performed:**
1. Creates authentication tables
2. Creates admin interface tables
3. Creates content types system tables
4. Creates session management tables

---

## 3. Create Migrations for Your Model

### Command
```bash
python manage.py makemigrations
```

**What this does:**
- Analyzes your models.py file
- Detects changes since the last migration
- Creates a new migration file in `posts/migrations/`
- Generates Python code to apply database changes

**Key Points:**
- Always run this after modifying your models
- Creates migration files like `0001_initial.py`
- Does NOT apply changes to the database yet
- Migration files are version control for your database schema

**Expected Output:**
```
Migrations for 'posts':
  posts/migrations/0001_initial.py
    - Create model Post
```

---

## 4. Apply the New Migration

### Command
```bash
python manage.py migrate
```

**What this does:**
- Applies the pending migrations to the database
- Creates the actual `posts_post` table in your database
- Updates Django's migration tracking system

**Important Notes:**
- This creates the actual database table
- The table name will be `posts_post` (app_name + model_name)
- Django automatically adds an `id` field as the primary key
- Always run migrate after makemigrations

**Expected Output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, posts, sessions
Running migrations:
  Applying posts.0001_initial... OK
```

---

## Migration Workflow Summary

The standard Django migration workflow:

1. **Modify your models** → Change models.py
2. **Create migrations** → `python manage.py makemigrations`
3. **Apply migrations** → `python manage.py migrate`

### Useful Migration Commands

```bash
# View migration status
python manage.py showmigrations

# View SQL that will be executed
python manage.py sqlmigrate posts 0001

# Create empty migration for custom operations
python manage.py makemigrations --empty posts
```

---

## Best Practices

- **Always create migrations** when you change models
- **Review migration files** before applying them
- **Never edit applied migrations** - create new ones instead
- **Keep migrations in version control**
- **Test migrations** on a copy of production data
- **Add helpful docstrings** to your models

---

## Next Steps

After completing this lesson, you should be able to:
- Define Django models with various field types
- Create and apply database migrations
- Understand the relationship between models and database tables
- Use the Django ORM to interact with your data

In the next lesson, we'll explore how to use the Django Admin interface to manage your Post model data.