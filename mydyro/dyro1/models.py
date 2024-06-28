from django.db import models
from django.utils.text import slugify
import itertools
import re  # Ensure re module is imported
from django.core.exceptions import ValidationError

# Create your models here.


class User(models.Model):
    ROLE_CHOICES = [
        ('regular', 'Regular User'),
        ('author', 'Author'),
        ('admin', 'Admin'),
    ]
    
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)  # Adjust max_length as needed
    email = models.EmailField(max_length=180)
    password = models.CharField(max_length=128)  # To store the hashed password
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='regular')
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'




class Contact(models.Model):
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()
    
    def __str__(self):
        return self.name
    
    
    
# ====================================
# category

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Use slugify to generate slug from name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
#==========================================================

# posts
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey('Category', related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
# ===========================================
# video

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    embed_code = models.TextField()  # Existing field for YouTube embed code
    code_snippet_name = models.CharField(max_length=200, blank=True, null=True)  # New field for code snippet name
    code_snippet = models.TextField(blank=True, null=True)  # New field for code snippet

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# =============================================
# comment
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    
    