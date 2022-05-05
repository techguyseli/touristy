from django import forms

class RegisterUserForm(forms.Form):
    csrfmiddlewaretoken = forms.CharField(required=True)
    username = forms.CharField(min_length=8, max_length = 40, required=True)
    password = forms.CharField(min_length=8, max_length = 40, required=True)
    password_repeat = forms.CharField(min_length=8, max_length = 40, required=True)