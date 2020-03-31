import xadmin
from django.contrib import admin

from .models import Comment


# @admin.register(Comment)
@xadmin.sites.register(Comment)
class CommentAdmin(object):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')

