from django.db import models
from Auth.models import UserProfile

# Create your models here.

class UploadedVideo(models.Model):
    user = models.ForeignKey(UserProfile)
    name = models.CharField(max_length=100)
    size = models.IntegerField(null=True, blank= True)
    video_file = models.FileField(upload_to=u'shalent/static/uploaded_video')

