from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)
    repPassword = forms.CharField(max_length=20)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)

class EditProfileForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField(required=False)