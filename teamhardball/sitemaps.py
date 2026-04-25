from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from comms.models import Post


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return [
            'home:index',
            'home:contact',
            'home:privacy_policy',
            'comms:post_list',
        ]

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Post.objects.order_by('-created_at')

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('comms:post_detail', args=[obj.slug])


sitemaps = {
    'static': StaticViewSitemap,
    'posts': PostSitemap,
}
