from django import forms

class AddForm(forms.Form):
    email = forms.EmailField()
    user_name = forms.CharField()
    pwd = forms.CharField()
