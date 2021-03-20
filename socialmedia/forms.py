from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)
    repPassword = forms.CharField(max_length=20)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)

class EditProfileForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('email',
                 'first_name',
                 'last_name'
                 )




class NewPostForm(forms.Form):
    content = forms.CharField(max_length=20)