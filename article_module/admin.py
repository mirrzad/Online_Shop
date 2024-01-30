from django.contrib import admin
from . import models


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'is_active', 'url_title']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'author']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super().save_model(request, obj, form, change)


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'parent', 'date']


admin.site.register(models.ArticleCategory, ArticleCategoryAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.ArticleComment, ArticleCommentAdmin)
