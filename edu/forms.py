from .models import Comment, Register
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )

class RegisterForm(forms.ModelForm):
  class Meta:
    model = Register
    fields = '__all__'