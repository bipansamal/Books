from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class About(models.Model):
    description = models.TextField()
    status = models.IntegerField()


class Profile(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  # Ensure proper relation
    title = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
