from django.db import models
from datetime import datetime

# Create your models here.

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
    listening_score = models.IntegerField(blank=True,null=True,default=0)
    reading_score = models.IntegerField(blank=True,null=True,default=0)
    score = models.IntegerField(blank=True,null=True,default=0)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.first_name} - {self.last_name} passed {self.quiz} and got {self.score}'