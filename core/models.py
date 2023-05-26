from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    id_user = models.IntegerField()
    username = models.CharField(max_length=100)
    age = models.IntegerField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    date_enrolled = models.DateTimeField(auto_now = True, blank = True, null=True)

    def __str__(self):
        return self.user.username
    
class Advocate(models.Model):
    username = models.CharField(max_length = 100)
    bio = models.TextField(null = True, blank = True)

    def __str__(self):
        return self.username