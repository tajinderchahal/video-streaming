from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(User):
    source = models.CharField(max_length=20)
    no_of_videos = models.IntegerField(default=0)
    

