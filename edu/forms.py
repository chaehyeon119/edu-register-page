from .models import Comment, JuniorRegister, ABCRegister, ClubRegister
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )

class JuniorRegisterForm(forms.ModelForm):
  class Meta:
    model = JuniorRegister
    fields = ['name', 'birthday', 'phone_number', 'school', 'grade', 'city', 'email', 'pro_exp', 'privacy', 'after_edu_ad']

class ABCRegisterForm(forms.ModelForm):
  class Meta:
    model = ABCRegister
    fields = '__all__'

class ClubRegisterForm(forms.ModelForm):
  class Meta:
    model = ClubRegister
    fields = ['name', 'team', 'email', 'phone_number', 'subject', 'file_upload']

