from django.db import models

# Create your models here.
class User(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField()
    date=models.DateTimeField(auto_now_add=True)

def __str__(self):
        return self.title