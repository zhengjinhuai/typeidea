import xadmin
from django.contrib import admin

from .models import Link, SideBar


# @admin.register(Link)
@xadmin.sites.register(Link)
class LinkAdmin(object):
    list_display = ['title', 'href', 'status', 'weight', 'created_time']
    fields = ('title', 'href', 'status', 'weight')
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)
    

# @admin.register(SideBar)
@xadmin.sites.register(SideBar)
class SideBarAdmin(object):
    list_display = ['title', 'display_type', 'content', 'created_time']
    fields = ('title', 'display_type', 'content')
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SideBarAdmin, self).save_model(request, obj, form, change)
