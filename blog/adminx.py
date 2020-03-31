from django.urls import reverse
from django.utils.html import format_html
# from django.contrib.admin.models import LogEntry

import xadmin
from xadmin.layout import Row, Fieldset, Container
from xadmin.filters import RelatedFieldListFilter, manager

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.base_admin import BaseOwnerAdmin


class PostInline(object):
    # fields = ('title', 'desc')
    form_layout = (
        Container(
            Row("title", "desc")
        )
    )
    extra = 1  # 控制额外多几个
    model = Post


# Register your models here.
# @admin.register(Category, site=custom_site)
@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


# class CategoryOwnerFilter(admin.SimpleListFilter):
class CategoryOwnerFilter(RelatedFieldListFilter):
    """ 自定义过滤器只展示当前用户分类 """
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        # test方法的作用是确认字段是否需要被当前的过滤器处理。
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获得lookup_choices,根据owner过滤
        self.lockup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


# 将过滤器注册到过滤器管理器中，并设置优先权，这样页面加载时会使用我们自定义的过滤器
manager.register(CategoryOwnerFilter, take_priority=True)


# @admin.register(Tag, site=custom_site)
@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


# @admin.register(Post, site=custom_site)
@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator'
    ]  # 配置列表展示内容
    list_display_links = []  # 可以作为链接的字段

    # list_filter = [CategoryOwnerFilter]  # 过滤数据的字段
    list_filter = ['category']  # 非filter类,而是字段名
    search_fields = ['title', 'category__name']  # 配置搜索字段

    actions_on_top = True  # 是否在顶部
    actions_on_bottom = True  # 是否在底部

    # 编辑页面
    save_on_top = True

    exclude = ['owner']

    fieldsets = (
        Fieldset(
            '基础信息',
            Row("title", "category"),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'content',
        ),
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    # class Media:
    #     # xadmin基于bootstrap，引入会页面样式冲突，仅供参考, 故注释。
    #     css = {
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )


# 因为xadmin自带log,所以这里可以去掉
# # @admin.register(LogEntry, site=custom_site)
# @xadmin.sites.register(LogEntry)
# class LogEntryAdmin(object):
#     list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
