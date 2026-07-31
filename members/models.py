from django.db import models

# Create your models here.
class Member(models.Model):
    country = models.CharField(max_length=1000)
    firstName = models.CharField(max_length=1000)
    lastName = models.CharField(max_length=1000)
    gender = models.CharField(max_length=100)
    dateOfBirth = models.CharField(max_length=200)
    classification = models.CharField(max_length=200)
    email = models.EmailField()