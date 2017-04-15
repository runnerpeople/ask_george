# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import IntegrityError
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import *
import re

# Create your forms here.

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        password = self.cleaned_data["password"]
        if password == " ":
            raise ValidationError("You must enter your password")
        return password

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    nickname = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())
    avatar = forms.ImageField()

    def validate(self):
        password = self.cleaned_data["password"]
        if password == " ":
            raise ValidationError("You must enter your password")
        password_confirm = self.cleaned_data["password_confirm"]
        if password_confirm == " ":
            raise ValidationError("You must confirm your password")
        if password != password_confirm:
            raise ValidationError("Passwords aren't equal!")
        avatar = self.cleaned_data["avatar"]
        if not avatar:
            avatar = "/uploads/1.jpg"

    def save(self):
        try:
            user = User.objects.create_user(self.cleaned_data["username"],self.cleaned_data["email"],make_password(self.cleaned_data["password"]))
            user.first_name = self.cleaned_data["nickname"]
            profile = Profile(user=user,avatar=self.cleaned_data["avatar"],name = user.first_name)
            user.save()
            profile.save()
        except IntegrityError:
            raise IntegrityError("This user already exists")

    def fill_form(self):
        for field in self.cleaned_data:
            self.fields[field].value = self.cleaned_data[field]

class SettingsForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    nickname = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(),required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput(),required=False)
    avatar = forms.ImageField()

    def validate(self):
        password = self.cleaned_data["password"]
        if password == " ":
            raise ValidationError("You must enter your password")
        password_confirm = self.cleaned_data["password_confirm"]
        if password_confirm == " ":
            raise ValidationError("You must confirm your password")
        if password != password_confirm:
            raise ValidationError("Passwords aren't equal!")
        avatar = self.cleaned_data["avatar"]
        if not avatar:
            avatar = "http://lorempixel.com/50/50/?v=284245"

    def save(self,profile):
        profile.user.first_name = self.cleaned_data["nickname"]
        profile.user.username = self.cleaned_data['username']
        if self.cleaned_data['password'] != '':
            profile.user.set_password(self.cleaned_data['password'])
        profile.user.email = self.cleaned_data['email']
        profile.user.save()
        profile.save()

class AskForm(forms.Form):
    title = forms.CharField(max_length=200)
    text = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(max_length=120)

    def clean_form(self):
        tags = self.cleaned_data["tags"]
        if not re.match("^[a-zA-Z0-9\,]*$", tags):
            raise ValidationError("Invalid characters in tags. Tags must separated by comma.")
        title = self.cleaned_data['title']
        if not Question.objects.get_question(title):
            raise forms.ValidationError('Question with current title already exist')

    def save(self,profile):
        tags_list = re.split('[\s,]+',self.cleaned_data["tags"])
        question = Question(title=self.cleaned_data["title"],text=self.cleaned_data["text"],date=timezone.now(),rating=0,profile=profile)
        question.save()
        for tag in tags_list:
            current_tag = Tag.objects.find_or_create(tag)
            current_tag.save()
            question.tags.add(current_tag)
        return question

class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

    def save(self, profile, question_id):
        question = Question.objects.get(pk=id)
        answer = Answer(question=question, text=self.cleaned_data['text'],
                        rating=0, date=timezone.now(), author=profile)
        answer.save()