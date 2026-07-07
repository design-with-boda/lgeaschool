from django.contrib import admin
from .models import NewsPost


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'is_featured', 'published_at']
    list_filter = ['category', 'is_published', 'is_featured']
    search_fields = ['title', 'content']
    list_editable = ['is_published', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
