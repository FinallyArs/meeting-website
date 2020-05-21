from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from meeting.models import User, Profile, Message


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label=u"Username")
    email = forms.EmailField(label=u"Email", required=True)
    password1 = forms.CharField(label=u"Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label=u"Confirm password", widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}







class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ['last_login', 'password', 'user', 'likes', 'last_online']


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size':'40','class': 'form-control'}))
    sender = forms.EmailField(widget=forms.TextInput(attrs={'size':'40','class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    copy = forms.BooleanField(required=False)


