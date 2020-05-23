from django import forms
from .models import Candidate, Comments
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms import Textarea
from voting.models import Profile
from django.forms import CharField, Form, PasswordInput


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ('name', 'surname', 'second_name', 'biography', 'election_programme', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class RegisterUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'] = CharField(widget=PasswordInput())

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].help_text = None


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['text'].widget = Textarea(attrs={'rows': 5})