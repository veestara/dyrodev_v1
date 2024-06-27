# myapp/forms.py

from django import forms
from .models import Category, Post
import re  # Ensure re module is imported
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .models import Video

class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=15)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    
# ===================================
# category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']
        widgets = {
            'slug': forms.TextInput(attrs={'placeholder': 'Leave blank to auto-generate'}),
        }

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if slug:
            # Replace spaces with hyphens
            slug = slugify(slug)
            # Validate the sanitized slug using the existing logic
            if not re.match(r'^[\w-]+$', slug):
                raise forms.ValidationError('Slug can only contain letters, numbers, underscores, or hyphens.')
        return slug
        
# ===================================
# posts

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'category', 'content', 'image', 'meta_description', 'meta_keywords']
        widgets = {
            'slug': forms.TextInput(attrs={'placeholder': 'Leave blank to auto-generate'}),
        }

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if slug:
            # Replace spaces with hyphens
            slug = slugify(slug)
            # Validate the sanitized slug using the existing logic
            if not re.match(r'^[\w-]+$', slug):
                raise forms.ValidationError('Slug can only contain letters, numbers, underscores, or hyphens.')
        return slug
# ====================================
# video
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'slug', 'embed_code', 'code_snippet_name', 'code_snippet']