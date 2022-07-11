from django.contrib import admin
from blog.models import *


# Register your models here.

class BlogerAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('pseudonym',)}
    list_display = ('id', 'pseudonym', 'slug', 'first_name', 'last_name', 'bio', 'age', 'is_published')
    list_display_links = ('id', 'pseudonym')
    search_fields = ('id', 'pseudonym', 'first_name', 'last_name')
    list_editable = ('is_published',)


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'slug', 'image', 'date_created', 'is_published', 'author')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_editable = ('is_published',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'discription', 'author', 'blog', 'date_create', 'is_published')
    list_display_links = ('id', 'discription')
    search_fields = ('author', 'blog', 'discription')
    list_editable = ('is_published',)


class ModelForTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(Blog, BlogAdmin)
admin.site.register(Bloger, BlogerAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ModelForTest, ModelForTestAdmin)
