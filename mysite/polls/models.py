from django.db import models
from django.utils import timezone
import datetime


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=40, null=False)
    id = models.AutoField(primary_key=True)
    age = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('the date published', auto_now_add=True)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Test(models.Model):
    context = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __Meta__(self):
        pass

    def __str__(self):
        return self.context
