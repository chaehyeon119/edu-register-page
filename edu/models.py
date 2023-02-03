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
    title = models.CharField(max_length=30, verbose_name="제목")
    hook_text = models.CharField(max_length=100, blank=True, verbose_name="부제")

    summary = models.CharField(max_length=30, verbose_name="요약 내용")
    content = MarkdownxField(verbose_name="내용")
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name="작성자")

    head_image = models.ImageField(upload_to='edu/images/%Y/%m/%d/', blank=True, verbose_name="대표 이미지")
    file_upload = models.FileField(upload_to='edu/files/%Y/%m/%d/', blank=True, verbose_name="파일 업로드")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="게시 일자")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정 일자")

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="카테고리")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="태그")

 

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

    
    class ProExpChoices(models.TextChoices):
        YES = "y", "유사교육을 수강한 적이 있습니다."
        NO = "n", "유사교육을 수강한 적이 없습니다."

    class SexChoices(models.TextChoices):
        FEMAIL = "f", "여성"
        MAIL = "m", "남성"
    
    class CityChoices(models.TextChoices):
        SEOUL = "seoul", "서울특별시"
        BUSAN = "busan", "부산광역시"
        DAEGU = "daegu", "대구광역시"
        INCHEON = "incheon", "인천광역시"
        GWANGJU = "gwanju", "광주광역시"
        DAEJUEON = "daejeon", "대전광역시"
        ULSAN = "ulsan", "울산광역시"
        SEJONG = "sejong", "세종특별자치시"
        GANGWON = "gangwon", "강원도"
        GYEONGI = "gyeongi", "경기도"
        GYEONGNAM = "gyeongnam", "경상남도"
        GYEONGBUK = "gyeongbuk", "경상북도"
        JEONNAM = "jeonnam", "전라남도"
        JEONBUK = "jeonbuk", "전라북도"
        JEJU = "jeju", "제주"
        CHUNGNAM = "chungnam", "충청남도"
        CHUNGBUK = "chungbuk", "충청북도"
        ETC = "etc", "기타"

        

    # 공통 항목
    id = models.AutoField(primary_key=True)
    register_time = models.DateTimeField(auto_now_add=True) # 신청 제출 일시
    name = models.CharField(max_length=10, verbose_name="이름") 
    birthday = models.CharField(max_length=10, verbose_name="생년월일", help_text="예) 030708")
    sex = models.CharField(max_length=1,
        choices=SexChoices.choices,
        verbose_name="성별")
    email = models.EmailField(max_length=100, verbose_name="이메일")

    phone_number = models.CharField(max_length=20, verbose_name="연락처", help_text="예) 010-1234-1234")

    city = models.CharField(max_length=10,
            choices=CityChoices.choices,
            verbose_name="현재 거주지") # 현재 거주지
    # ex: JuniorRegister.objects.filter(sex=Register.SexChoices.FEMAIL)
    privacy = models.BooleanField(verbose_name="개인정보 및 초상권 사용 동의", default=True, null=False, help_text="[개인정보 및 초상권 사용 동의] 입력해주신 개인정보는 교육 과정을 운영하는 목적으로 이용하며, 참여자 사진/영상 촬영과 수집 및 활용에 동의합니다.") # 개인정보 동의서 체크 (필수)
    after_edu_ad = models.BooleanField(verbose_name="추후 교육 소식 안내", default=True, help_text="동의 시, 주니어 데이터 분석 교실 및 다양한 데이터 활용 교육 프로그램 개설 소식을 안내드립니다.") # 추후, 교육 소식 받는지 여부 (선택)
    sent_day = models.DateTimeField(auto_now=True, verbose_name="접수 일자")

    class Meta:
        abstract = True

    # 선택항목(주니어)
class JuniorRegister(Register):
    class GradeChoices(models.TextChoices):
        THIRD = "ele_third", "초등학교 3학년"
        FOUTH = "ele_fouth", "초등학교 4학년"
        FIFTH = "ele_fifth", "초등학교 5학년"
        SIXTH = "ele_sixth", "초등학교 6학년"
        MIDFIRST = "mid_first", "중학교 1학년"
        MIDSECOND = "mid_second", "중학교 2학년"
        MIDTHRID = "mid_thrid", "중학교 3학년"
        ETC = "etc", "기타"

    class ProExpChoices(models.TextChoices):
        YES = "y", "이전에 수강한 적이 있습니다."
        NO = "n", "첫 수강입니다."

    school = models.CharField(max_length=200, help_text="OOO초등학교", verbose_name="학교명") # 학교
    grade = models.CharField(max_length=10,
            choices=GradeChoices.choices,
            verbose_name="학년") # 학년

    parents_phone = models.CharField(max_length=20, verbose_name="부모님 연락처", help_text="예) 010-1234-1234"),
    pro_exp = models.CharField(max_length=1, choices=ProExpChoices.choices, default=ProExpChoices.YES, verbose_name="주니어 수강 경험 여부")

    def __str__(self):
        return f'[{self.pk}] {self.name}' #해당 포스트의 pk값과 title이 나옴 ex [1]첫번째 포스트


    # 선택항목(ABC 부트캠프)
class ABCRegister(Register):
    class ABCRegisterWayChoices(models.TextChoices):
        RECOMMAND = "recommand", "지인 추천"
        NAVERCAFE = "navercafe", "네이버 카페"
        EVERYTIME = "everytime", "에브리타임"
        SNS ="sns", "인스타그램/페이스북"
        MAJORCONTACT = "major_contact", "학과 이메일/문자"
        UNIVINFO = "univinfo", "대학 게시판"
        POSTER ="poster", "포스터"
        BUSSTOP = "busstop", "버스 정류장 광고"
        ETC = "etc", "기타"

    
    class GradeChoices(models.TextChoices):
        HIGHGRADUATE = "high_grad", "고등학교 졸업"
        UNIVFIRSTING = "univ_first_ing", "대학 1학년 재학중"
        UNIVSECONDING = "univ_second_ing", "대학 2학년 재학중"
        UNIVTHRIDING = "univ_thrid_ing", "대학 3학년 재학중"
        UNIVFOUTHING = "univ_fouth_ing", "대학 4학년 재학중"
        UNIVREST = "univ_rest", "대학 휴학중"
        UNIVQUIT ="univ_quit", "대학 중퇴"
        UNIVGRADUATE = "univ_grad", "대학 졸업"
        GRADUATIONSCHOOLING = "graduation_schoo_ling", "대학원 재학중"
        GRADUATIONSCHOOLGRAD = "graduation_school_grad", "대학원 졸업"
        ETC = "etc", "기타"

    class ProExpChoices(models.TextChoices):
        YES = "y", "유사교육을 수강한 적이 있습니다."
        NO = "n", "유사교육을 수강한 적이 없습니다."

    school = models.CharField(max_length=200, help_text="학교명") # 학교
    grade = models.CharField(max_length=30,
            choices=GradeChoices.choices,
            verbose_name="학년"
    ) # 학년
    register_way = models.CharField(max_length=20, choices=ABCRegisterWayChoices.choices, verbose_name="신청경로")
    school_city = models.CharField(max_length=100) # 학교 소재지 서울특별시, 대전특벌시 .... 기타
    recommender = models.CharField(max_length=100 ,null=True) #교육 추천자
    pro_exp = models.CharField(max_length=1, choices=ProExpChoices.choices, default=ProExpChoices.YES, verbose_name="유사 교육 수강 여부")
    pro_name = models.CharField(max_length=100, blank=True, verbose_name="유사 교육명", help_text="유사교육을 수강하신 적이 있다면, 수강교육명을 써주세요.")
    
    self_intro = models.TextField() # 자기소개
    self_motive = models.TextField()  # 지원동기
    info_noshow = models.CharField(max_length=1) # 노쇼시 불이익 확인 체크 (필수)

