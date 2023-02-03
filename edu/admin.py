from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Category, Tag, Comment,JuniorRegister


admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Comment)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}   

class JuniorRegisterAdmin(admin.ModelAdmin):
    list_display = ['id','sent_day', 'name', 'birthday', 'school', 'sex', 'city', 'email', 'after_edu_ad', 'privacy']
    search_fields = ['']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(JuniorRegister, JuniorRegisterAdmin)