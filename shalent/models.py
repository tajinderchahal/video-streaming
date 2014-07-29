from django.db import models
from Auth.models import UserProfile

# Create your models here.

class UploadedVideo(models.Model):
    user = models.ForeignKey(UserProfile)
    name = models.CharField(max_length=100)
    size = models.IntegerField(null=True, blank= True)
    video_file = models.FileField(upload_to=u'shalent/static/uploaded_video')

class UserType(models.Model):
    user_type = models.CharField(max_length=100)

class UserCategory(models.Model):
    category_type = models.CharField(max_length=100)
    user_type = models.ForeignKey(UserType, null=True, blank= True)
class MasterUserCategory(models.Model):
    user_profile = models.ForeignKey(UserProfile, null=True, blank= True)
    user_category= models.ForeignKey(UserCategory, null=True, blank= True)