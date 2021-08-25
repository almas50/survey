from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser


class Survey(models.Model):
    name = models.CharField(help_text="name of survey", max_length=100)
    start_date = models.DateField(help_text="start date of survey")
    end_date = models.DateField(help_text="end date of survey")
    description = models.TextField()


class Question(models.Model):
    Type_of_Question = [('Text', 'Text'),
                     ('One_Answer', 'One_Answer'),
                     ('Multi_Answer', 'Multi_Answer')]
    text = models.TextField(help_text="text of question")
    type = models.CharField(help_text="type of question", choices=Type_of_Question, max_length=100)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions', default=None)


class Response(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='responses')
    created = models.DateTimeField(blank=True, auto_now_add=True)


class Answers(models.Model):
    text = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name="answers")


class Option(models.Model):
    text = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    correct = models.BooleanField()

