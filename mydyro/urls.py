from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from dyro1.sitemap import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

# Define your urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dyro1.urls')),  # Include the app's URLs

    # Define the sitemap URL
    
# ------------------------------------------------------
    # 20/06/2024
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
# ------------------------------------------------------

]
