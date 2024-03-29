from django.contrib import admin
from webapp.models import Article, Comment, Category


class CommentAdmin(admin.TabularInline):
    model = Comment
    fields = ['author', 'text']
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'author', 'created_at']
    list_filter = ['author', 'category']
    list_display_links = ['pk', 'title']
    search_fields = ['title', 'text']
    exclude = []
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CommentAdmin]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    list_display_links = ['pk', 'name']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Category)
