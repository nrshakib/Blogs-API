from django.contrib import admin

from posts.models import PostModel

@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'author', 'status']
    search_fields = ['title', 'author__username', 'author__email']
    list_filter = ['status']

