from django import forms

class NearbyForm(forms.Form):
    csrfmiddlewaretoken = forms.CharField()
    latitude = forms.DecimalField(max_digits=20, decimal_places=17)
    longitude = forms.DecimalField(max_digits=20, decimal_places=17)