from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    ROLE_CHOICES = [
        ('SDE', 'Software Engineer'),
        ('DA', 'Data Analyst'),
        ('PM', 'Product Manager'),
    ]
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    difficulty = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Question(models.Model):
    TYPE_CHOICES = [
        ('technical', 'Technical'),
        ('behavioral', 'Behavioral'),
    ]
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    difficulty = models.CharField(max_length=20)

    def __str__(self):
        return self.question_text[:50]

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.topic.name} - {self.score}"

