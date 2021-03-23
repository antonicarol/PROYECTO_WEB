from django import forms
from django.contrib.auth.models import User

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',
                 'first_name',
                 'last_name'
                 )

class NewUserForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    repeatPassword = forms.CharField(widget=forms.PasswordInput())

    prefix = "new_user_form"

class LoginUserForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())


class NewPostForm(forms.Form):
    content = forms.CharField(max_length=20)

class EditPostForm(forms.Form):
    content = forms.CharField(max_length=20)

class FollowUserForm(forms.Form):
    username = forms.CharField(widget=forms.HiddenInput(),max_length=20)
    action = forms.IntegerField(widget=forms.HiddenInput())
