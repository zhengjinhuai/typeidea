from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed

from .models import Post


class ExtendedRSSFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement('content:html', item('content_html'))


class LatestPostFeed(Feed):
    """
    默认情况下，使用RSS 2.0类型，如果要指定类型，在Feed类中添加feed_type属性，如下所示：
        django.utils.feedgenerator.Rss201rev2Feed (RSS 2.01. Default.)
        django.utils.feedgenerator.RssUserland091Feed (RSS 0.91.)
        django.utils.feedgenerator.Atom1Feed (Atom 1.0.)
        在一个 RSS feed中，每一个<item>都有一个<title>, <link> 和<description>， 我们需要告诉框架往这些对象里放入哪些数据。
    """

    feed_type = Rss201rev2Feed
    title = "Typeidea Blog System"
    link = "/rss/"
    description = "Typeidea is a blog system power by django"

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc

    def item_link(self, item):
        return reverse('post-detail', args=[item.pk])
