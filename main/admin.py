from django.contrib import admin

from .models import *


class ImageInline(admin.TabularInline):
    model = CodeImage
    max_num = 7
    min_num = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ]


admin.site.register(Reply)
admin.site.register(Comment)
