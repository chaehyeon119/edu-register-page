from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Category, Tag, Comment,JuniorRegister, ClubRegister
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin



admin.site.register(Comment)
admin.site.register(ClubRegister)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}   

class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'hook_text', 'content', 'category', 'tags', 'created_at', 'updated_at']


class JuniorRegisterAdmin(admin.ModelAdmin):
    list_display = ['id','sent_day', 'name', 'birthday', 'school', 'sex', 'city', 'email', 'after_edu_ad', 'privacy']
    search_fields = ['id','sent_day', 'name', 'birthday', 'school', 'sex', 'city', 'email', 'after_edu_ad', 'privacy']

class ClubRegisterAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'team', 'email', 'phone_number', 'subject', 'file_upload', 'register_time']
    

# class JuniorRegisterExcel(ImportExportMixin, admin.ModelAdmin):
#     pass

# admin.site.register(JuniorRegisterExcel) => MediaDefiningClass

admin.site.register(Post, MarkdownxModelAdmin)
# admin.site.register(PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(JuniorRegister, JuniorRegisterAdmin)
