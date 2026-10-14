from django.db import models
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Member(models.Model):
    country = models.CharField(max_length=1000)
    firstName = models.CharField(max_length=1000)
    lastName = models.CharField(max_length=1000)
    gender = models.CharField(max_length=100)
    dateOfBirth = models.CharField(max_length=200)
    classification = models.CharField(max_length=200)
    email = models.EmailField()




class Profile(models.Model):
    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_USER, 'User'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


# Auto-create a Profile whenever a new account is made.
# Superusers (createsuperuser) automatically become ADMIN, everyone else USER.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            role=Profile.ROLE_ADMIN if instance.is_superuser else Profile.ROLE_USER,
        )