from django.db import models

# Create your models here.

class About(models.Model):
    description = models.TextField()
    status = models.IntegerField()
    