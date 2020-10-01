from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rank = models.CharField(max_length=50)
    def teacher_id(self):
        return f'{self.rank} {self.user.last_name}'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class Quiz(models.Model):
    title = models.CharField(max_length=50)
    audio = models.FileField(upload_to='audio/')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.CharField(max_length=1,choices=([('a','a'),('b','b'),('c','c'),('d','d'),]))
    choice1 = models.TextField()
    choice2 = models.TextField()
    choice3 = models.TextField()
    choice4 = models.TextField()

    def __str__(self):
        return self.question

class Student(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50,null=True, blank=True)
    instructor = models.CharField(max_length=50,null=True, blank=True)
    service = models.CharField(max_length=50,null=True, blank=True)
    rank = models.CharField(max_length=50,null=True, blank=True)
    listening_score = models.IntegerField(blank=True,null=True,default=0)
    reading_score = models.IntegerField(blank=True,null=True,default=0)
    score = models.IntegerField(blank=True,null=True,default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} - {self.last_name} passed {self.quiz} and got {self.score}'