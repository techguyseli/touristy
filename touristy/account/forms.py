from django import forms

class RegisterUserForm(forms.Form):
    csrfmiddlewaretoken = forms.CharField(required=True)
    username = forms.CharField(min_length=5, max_length = 40, required=True)
    password = forms.CharField(min_length=8, max_length = 40, required=True)
    password_repeat = forms.CharField(min_length=8, max_length = 40, required=True)

    def passwords_match(self):
        if self.cleaned_data['password'] == self.cleaned_data['password_repeat']:
            return True
        return False