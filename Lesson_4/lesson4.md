# Django Lesson 4: Django ORM Basics

## Overview
This lesson covers the very basics of Django ORM (Object-Relational Mapping) using the Django shell. We'll learn how to create, save, and query Post objects using Python code.

---

## 1. Accessing Django Shell

### Command
```bash
python manage.py shell
```

**What this does:**
- Opens an interactive Python shell with Django environment loaded
- Automatically imports Django settings and configurations
- Allows you to interact with your models directly
- Useful for testing and debugging

---

## 2. Working with the Post Model

### Import the Post Model
```python
from posts.models import Post
```

**What this does:**
- Imports the Post class from your posts app's models module
- Makes the Post model available for ORM operations

---

## 3. Creating Your First Post Object

### Creating a Post Instance
```python
p = Post()
```

**What this does:**
- Creates a new instance of the Post model
- Object exists in memory but NOT yet saved to database
- All fields are empty/default values

---

## 4. Setting Post Attributes

### Adding Data to Post Fields
```python
p.title = "My First Post!"
p.save()
```

**What this does:**
- **p.title**: Sets the title field of the post
- **p.save()**: Saves the post object to the database
- Generates an INSERT SQL statement
- Auto-generates the `id` and `date` fields

**Important Notes:**
- `save()` is required to persist data to database
- `date` field auto-populates due to `auto_now_add=True`
- Django auto-assigns an `id` (primary key)

---

## 5. Querying All Post Objects

### Get All Posts
```python
Post.objects.all()
```

**Output:**
```
<QuerySet [<Post: My First Post!>]>
```

**What this does:**
- Returns a QuerySet containing all Post objects
- QuerySet is Django's way of representing database queries
- Shows the `__str__()` method output for each object

---

## 6. Creating a Second Post Object

### Complete Post Creation Example
```python
p = Post()
p.title = "My 2nd Post"
p.save()
```

**What this does:**
- Creates another Post instance
- Sets the title field
- Saves it to the database

---

## 7. Querying Multiple Objects

### View All Posts Again
```python
Post.objects.all()
```

**Output:**
```
<QuerySet [<Post: My First Post!>, <Post: My 2nd Post>]>
```

**What this shows:**
- Now we have 2 Post objects in the database
- Both posts are displayed in the QuerySet
- Each post shows its title (due to `__str__()` method)

---

## Key Django ORM Concepts Learned

### Model Instance Operations
- **Creating**: `p = Post()` - Creates new instance in memory
- **Setting Fields**: `p.title = "value"` - Assigns values to fields
- **Saving**: `p.save()` - Persists object to database

### QuerySet Operations
- **objects.all()**: Returns all objects as a QuerySet
- **QuerySet**: Django's representation of database query results
- **Lazy Evaluation**: Queries execute only when data is needed

### Auto-Generated Fields
- **id**: Primary key automatically created by Django
- **date**: Auto-populated when `auto_now_add=True` is set

---

## Django Shell Tips

### Useful Shell Commands
```python
# Exit the shell
exit()

# Import multiple models
from posts.models import Post, Comment

# Check object attributes
p.__dict__  # Shows all field values

# Get object count
Post.objects.count()
```

### Shell Session Management
- Use `Ctrl+D` or `exit()` to leave the shell
- Each shell session is independent
- Changes persist in the database between sessions

---

## What We Accomplished

In this lesson, we successfully:
1. **Opened Django shell** and imported our Post model
2. **Created Post objects** using the ORM
3. **Set field values** and saved objects to database
4. **Queried the database** to retrieve all posts
5. **Verified data persistence** across operations

---

## Next Steps

After mastering these basics, you'll be ready to learn:
- More complex queries (filtering, ordering)
- Relationship fields (ForeignKey, ManyToMany)
- Django Admin interface for easier data management
- Views that display this data on web pages

The Django ORM provides a powerful, Pythonic way to work with databases without writing SQL directly!