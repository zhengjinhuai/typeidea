# from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from dal import autocomplete
from django import forms

from .models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='category-autocomplete'),
        label='分类',
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签',
    )
    # content = forms.CharField(widget=CKEditorWidget(), label='正文', required=True)
    content_ck = forms.CharField(widget=CKEditorUploadingWidget(), label='正文', required=True)
    content_md = forms.CharField(widget=forms.Textarea(), label='正文', required=True)
    content = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Post
        # 其实最后的class Meta可以不配置，但是为了避免出现JavaScript 资源冲突的问题，我们
        # 还是定义了Meta以及其中的fields，需要把自动补全的字段放到前面。
        fields = ('category', 'tag', 'title', 'desc',
                  'is_md', 'content', 'content_md', 'content_ck',
                  'status')

    def __init__(self, instance=None, initial=None, **kwargs):
        # 对From进行初始化处理
        """

        :param instance: 假如编辑的是一篇文章,则参数为当前文章实例
        :param initial:
        :param kwargs:
        """
        initial = initial or {}
        if instance:
            if instance.is_md:
                initial['content_md'] = instance.content
            else:
                initial['content_ck'] = instance.content

        super(PostAdminForm, self).__init__(instance=instance, initial=initial, **kwargs)

    def clean(self):
        """判断是否使用了Markdown语法, 然后设置获取对应编辑器的值，井将其赋值给content 。"""
        is_md = self.cleaned_data.get('is_md')
        if is_md:
            content_field_name = 'content_md'
        else:
            content_field_name = 'content_ck'
        content = self.cleaned_data.get(content_field_name)
        if not content:
            self.add_error(content_field_name, '必填项!')
            return
        self.cleaned_data['content'] = content
        return super().clean()

    class Media:
        js = ('js/post_editor.js')

