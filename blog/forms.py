from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, Textarea, Select

from blog.models import Comment, Blog


class AddComent(ModelForm):
    class Meta:
        model = Comment
        fields = ['discription']
        widgets = {
            "content": Textarea(attrs={
                'class': 'form_comment',
                'placeholder': 'enter you comment'
            }),
            "author": Select(attrs={
                'class': 'form_comment'})}


class AddBlog(ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'discription']
        widgets = {
            "title": Textarea(attrs={
                'class': 'form_comment',
                'placeholder': 'Blog name'
            }),
            'discription': Textarea(attrs={
                'class': 'form-comment',
                'placeholder': 'Blog content'})}


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'register_form'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'register_form'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'register_form'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'register_form'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'register_form'}))
