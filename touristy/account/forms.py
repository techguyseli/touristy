from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=70)
    password = forms.CharField(label='Password', max_length=70)
    password_confirmation = forms.CharField(label='Repeat password', max_length=70)