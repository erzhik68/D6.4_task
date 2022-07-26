from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment, Subscriber

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id", "category_name")
    # fieldsets = (
    #     ("Subscribers", {
    #         "classes": ("collapse",),
    #         "fields": (("subscribers",),)
    #     }),
    # )

admin.site.register(Author)
admin.site.register(Subscriber)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
