from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ['home', 'about']
    
    # def items(self):
    #     return YourModel.objects.all()  # Replace YourModel.objects.all() with your queryset

    # def lastmod(self, obj):
    #     return obj.modified_date

    def location(self, item):
        return reverse(item)
