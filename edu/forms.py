from .models import Comment, JuniorRegister, ABCRegister
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )

class JuniorRegisterForm(forms.ModelForm):
  class Meta:
    model = JuniorRegister
    fields = '__all__'

class ABCRegisterForm(forms.ModelForm):
  class Meta:
    model = ABCRegister
    fields = '__all__'