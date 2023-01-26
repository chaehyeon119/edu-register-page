from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from makrdownx.utils import markdown
import os

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True) # 같은 name의 동일한 카테고리 생성 불가
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/edu/tag/{self.slug}/'
    


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True) # 같은 name의 동일한 카테고리 생성 불가
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/edu/category/{self.slug}/'
    
    class Meta:
        verbose_name_plural = 'Categories'

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = MarkdownxField()
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    head_image = models.ImageField(upload_to='edu/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='edu/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}] {self.title}' #해당 포스트의 pk값과 title이 나옴 ex [1]첫번째 포스트

    def get_absolute_url(self):
        return f'/edu/{self.pk}/'
    
    def get_file_name(self): #파일명
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self): #확장자
        return self.get_file_name().split('.')[-1]
    
    def get_content_markdown(self):
        return markdown(self.content)

# class Post(models.Model):
#     title = models.CharField(max_length=30)
#     hook_text = models.CharField(max_length=100, blank=True)
#     content = MarkdownxField()

#     head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
#     file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

#     category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
#     tags = models.ManyToManyField(Tag, blank=True)

#     def __str__(self):
#         return f'[{self.pk}]{self.title} :: {self.author}'

#     def get_absolute_url(self):
#         return f'/blog/{self.pk}/'

#     def get_file_name(self):
#         return os.path.basename(self.file_upload.name)

#     def get_file_ext(self):
#         return self.get_file_name().split('.')[-1]

#     def get_content_markdown(self):
#         return markdown(self.content)

#     def get_avatar_url(self):
#         if self.author.socialaccount_set.exists():
#             return self.author.socialaccount_set.first().get_avatar_url()
#         else:
#             return f'https://api.adorable.io/avatars/60/{self.author.username}.png'

