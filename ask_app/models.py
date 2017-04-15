# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.db import IntegrityError
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
import datetime
import re

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to="avatars/")

    name = models.CharField(max_length=60)

    def __unicode__(self):
        return self.name

class TagManager(models.Manager):


    def find(self,name):
        return self.get(name=name)

    def find_or_create(self,name):
        tag = ""
        try:
            tag = self.get(name=name)
        except:
            tag = self.create(name=name)
        finally:
            return tag


class Tag(models.Model):
    name = models.CharField(max_length=30,default="Test")

    objects = TagManager()

    def get_url(self):
        reverse("tag", kwargs={"tag": self.name})

    def __unicode__(self):
        return self.name


class QuestionQuerySet(models.QuerySet):

    def popular(self):
        return self.order_by("-rating")

    def later_date(self,date):
        return self.filter(published__gt=date)

class QuestionManager(models.Manager):

    def get_queryset(self):
        return QuestionQuerySet(self.model,using=self._db)

    def new(self):
        return self.order_by("-published")

    def like(self):
        return self.order_by("-rating")

    def tag(self,tag):
        return self.filter(tags=tag)

    def best(self):
        week = timezone.now() + datetime.timedelta(days=-7)
        return self.get_queryset().popular().later_date(week)

    def get_question(self,title):
        return self.filter(title=title)

class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(default=" ")
    published = models.DateField(default=timezone.now())
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Profile,null=True)
    rating = models.IntegerField(default=0, verbose_name="Rating")

    objects = QuestionManager()

    class Meta:
        ordering = ["-published","-rating"]

    def get_url(self):
        reverse("question",kwargs={"question_id":self.id})

    def __unicode__(self):
        return self.title

class LikeManager(models.Manager):
    def update_like(self, question=None,answer=None):
        if question != None:
            return self.filter(question=question).aggregate(sum=models.Sum('value'))['sum']
        elif answer != None:
            return self.filter(answer=answer).aggregate(sum=models.Sum('value'))['sum']

    def create_or_update(self,author,value=0, answer = None, question = None):
        if answer == None and question != None:
            obj, new = self.update_or_create(question=question, author=author, value=value)
            question.rating = self.update_like(question=question)
            question.save()
            return new
        elif answer != None and question == None:
            obj, new = self.update_or_create(answer=answer, author=author, value=value)
            answer.rating = self.update_like(answer=answer)
            question.save()
            return new


class QuestionLike(models.Model):
    question = models.ForeignKey(Question)
    author = models.ForeignKey(Profile)
    value = models.IntegerField(default=0)

    objects = LikeManager()

class AnswerQuerySet(models.QuerySet):
    def popular(self):
        return self.order_by("-rating")

    def later_date(self, date):
        return self.filter(published__gt=date)

class AnswerManager(models.Manager):

    def get_queryset(self):
        return AnswerQuerySet(self.model, using=self._db)

    def get_question(self,question):
        return self.filter(question=question)

    def best(self):
        week = timezone.now() + datetime.timedelta(days=-7)
        return self.get_queryset().popular().later_date(week)

class Answer(models.Model):
    text = models.TextField(default=" ")
    question = models.ForeignKey(Question,null=True)
    is_correct = models.BooleanField(default=False)
    author = models.ForeignKey(Profile,null=True)
    published = models.DateField(default=timezone.now())
    rating = models.IntegerField(default=0, verbose_name="Rating")

    objects = AnswerManager()

    class Meta:
        ordering = ["-published", "-rating","-is_correct"]


    def __unicode__(self):
        return self.text

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer)
    author = models.ForeignKey(Profile)
    value = models.IntegerField(default=0)

    objects = LikeManager()












