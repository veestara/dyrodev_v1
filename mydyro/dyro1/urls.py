# ------------------------------------------------------
    # 20/06/2024
from django.urls import path
from . import views
from .sitemap import StaticViewSitemap
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static



sitemaps = {
    'static': StaticViewSitemap, 

}

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('work/', views.work, name='work'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('otp/', views.otp, name='otp'),
    path('forget/', views.forget, name='forget'),
    path('reset/', views.reset, name='reset'),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap",),
    path('success/', TemplateView.as_view(template_name='success.html'), name='success'),
    path('error/', TemplateView.as_view(template_name='error.html'), name='error'),
    path('sunpac_view/', views.sunpac_view, name='sunpac_view'),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
# ------------------------------------------------------


# Post URLs
    path('posts/', views.post_list, name='post_list'),
    path('add-post/', views.post_add, name='post_add'),
    path('posts/<slug:slug>/update/', views.post_update, name='post_update'),
    path('posts/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    
# ======================================================
# comment
    path('post/<slug:slug>/add_comment/', views.add_comment, name='add_comment'),
    
    
# ======================================================
# video
    path('videos/', views.video_list, name='video_list'),
    path('video/create/', views.video_create, name='video_create'),
    path('video/update/<int:pk>/', views.video_update, name='video_update'),
    path('video/delete/<int:pk>/', views.video_delete, name='video_delete'),
    path('video/<slug:slug>/', views.video_detail, name='video_detail'),  

# ======================================================

# category
    path('category-list/', views.category_list, name='category_list'),
    path('add-category/', views.category_add, name='category_add'),
    path('<slug:slug>/update/', views.category_update, name='category_update'),
    path('<slug:slug>/delete/', views.category_delete, name='category_delete'),
    path('<slug:slug>/', views.category_detail, name='category_detail'),
#  =====================================================


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
