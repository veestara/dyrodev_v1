from django.contrib import admin
from django.core.cache import cache
from django.contrib import messages
from .models import *

# admin.site.register(Contact)

def clear_cache(modeladmin, request, queryset):
    cache.clear()
    modeladmin.message_user(request, "Cache cleared successfully", messages.SUCCESS)

clear_cache.short_description = "Clear Cache"

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    actions = [clear_cache]
    


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    actions = [clear_cache]
    
    
    
    
    
    




