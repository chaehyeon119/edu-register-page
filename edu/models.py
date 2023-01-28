from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
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

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1433/7d5d616e1a67d0cd/svg/{self.author.email}'



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'


    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1433/7d5d616e1a67d0cd/svg/{self.author.email}'


class Register(models.Model) :
    # 공통 항목
    id = models.AutoField(primary_key=True)
    register_time = models.DateTimeField(auto_now_add=True) # 신청 제출 일시
    name = models.CharField(max_length=10) 
    birthday = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    city = models.CharField(max_length=100) # 현재 거주지
    school = models.CharField(max_length=200) # 학교
    grade = models.CharField(max_length=50) # 학년
    register_way = models.CharField(max_length=200) # 신청경로
    pro_exp = models.CharField(max_length=1, null=True) # 유사교육 수강 여부 yes or no
    pro_name = models.CharField(max_length=100, null=True) # yes일 경우, 수강 교육명
    
    privacy = models.CharField(max_length=1) # 개인정보 동의서 체크 (필수)
    after_edu_ad = models.CharField(max_length=1, null=True) # 추후, 교육 소식 받는지 여부 (선택)

    # 선택항목(주니어)
    parents_phone = models.CharField(max_length=100)

    # 선택항목(ABC 부트캠프)
    school_city = models.CharField(max_length=100) # 학교 소재지 서울특별시, 대전특벌시 .... 기타
    recommender = models.CharField(max_length=100 ,null=True) #교육 추천자
    self_intro = models.TextField() # 자기소개
    self_motive = models.TextField()  # 지원동기
    info_noshow = models.CharField(max_length=1) # 노쇼시 불이익 확인 체크 (필수)
    