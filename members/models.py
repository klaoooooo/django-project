from django.db import models

# Create your models here.
class Member(models.Model):
    country = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    dateOfBirth = models.CharField(max_length=20)
    classification = models.CharField(max_length=20)
    email = models.EmailField()