from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('User not find')
            if not user.check_password(password):
                raise forms.ValidationError('false password')
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)
    re_password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               required=False)


    class Meta:
        model = User
        fields = ('username', )


    def clean_re_password(self, *args, **kwargs):
        data = self.cleaned_data
        if data['password'] != data['re_password']:
            raise forms.ValidationError('Wrong repeat password')
        return data['re_password']