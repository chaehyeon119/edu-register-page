from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Category, Tag, Comment,JuniorRegister


admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Comment)
admin.site.register(JuniorRegister)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}   

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
