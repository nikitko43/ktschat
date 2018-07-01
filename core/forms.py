from django import forms
from django.contrib import auth
from django.contrib.auth.forms import UsernameField, AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from core.models import Message

class LoginForm(AuthenticationForm):
    username = UsernameField(max_length=64,
                             widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': "Введите имя пользователя"}))
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Введите пароль"})
    )


class ChatUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'attached_file']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        message = super().save(commit=False)
        message.author = self.user
        if commit:
            message.save()

        return message
