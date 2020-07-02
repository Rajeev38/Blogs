from django.forms import ModelForm
from django import forms
from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignupForm(ModelForm):
    password1 = forms.CharField(max_length=50,widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = '__all__'
        widgets = {'password': forms.PasswordInput}

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password'].required = True
        self.fields['username'].required = True

    # def user_check(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #     password1 = self.cleaned_data.get('password')
    #     email = self.cleaned_data.get('email')
    #
    #     if User.objects.filter(username=username).exists():
    #         raise ValidationError("Email already exists")
    #     return username