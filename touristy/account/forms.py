from django import forms

class RegisterUserForm(forms.Form):
    csrfmiddlewaretoken = forms.CharField()
    username = forms.CharField(min_length=5, max_length = 40)
    password = forms.CharField(min_length=8, max_length = 40)
    password_repeat = forms.CharField(min_length=8, max_length = 40)

    def passwords_match(self):
        if self.cleaned_data['password'] == self.cleaned_data['password_repeat']:
            return True
        return False


class ChangeUsernameForm(forms.Form):
    csrfmiddlewaretoken = forms.CharField()
    username = forms.CharField(min_length=5, max_length = 40)


class ChangePasswordForm(forms.Form):
    csrfmiddlewaretoken = forms.CharField()
    old_password = forms.CharField(min_length=8, max_length = 40)
    new_password = forms.CharField(min_length=8, max_length = 40)
    password_repeat = forms.CharField(min_length=8, max_length = 40)

    def new_passwords_match(self):
        if self.cleaned_data['new_password'] == self.cleaned_data['password_repeat']:
            return True
        return False

    def password_changed(self):
        if self.cleaned_data['new_password'] == self.cleaned_data['old_password']:
            return False
        return True


class AddServiceForm(forms.Form):
    csrfmiddlewaretoken = forms.CharField()
    title = forms.CharField(min_length=1, max_length = 60)
    type = forms.CharField(min_length=1, max_length = 20)
    latitude = forms.DecimalField(max_digits=20, decimal_places=17)
    longitude = forms.DecimalField(max_digits=20, decimal_places=17)


class ModifyServiceForm(forms.Form):
    csrfmiddlewaretoken = forms.CharField()
    service_id = forms.IntegerField()
    title = forms.CharField(min_length=1, max_length = 60)
    type = forms.CharField(min_length=1, max_length = 20)
    latitude = forms.DecimalField(max_digits=20, decimal_places=17)
    longitude = forms.DecimalField(max_digits=20, decimal_places=17)


class AddImageForm(forms.Form):
    csrfmiddlewaretoken = forms.CharField()
    service_id = forms.IntegerField()
    image_url = forms.CharField(max_length=300)


class AddRatingForm(forms.Form):
    csrfmiddlewaretoken = forms.CharField()
    stars = forms.IntegerField(min_value=1, max_value=5)
    service_id = forms.IntegerField()
    comment = forms.CharField()