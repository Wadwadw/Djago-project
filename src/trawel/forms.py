from django import forms
from django.contrib.auth import authenticate

class UserLoginForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        user_name = self.cleaned_data.get('user_name')
        password = self.cleaned_data.get('password')

        if user_name and password:
            user = authenticate(user_name=user_name, password=password)
            if not user:
                raise forms.ValidationError('User not find')
            if not user.check_password(password):
                raise forms.ValidationError('false password')
        return super(UserLoginForm, self).clean(*args, **kwargs)