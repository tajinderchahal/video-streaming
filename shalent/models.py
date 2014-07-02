from django.db import models

# Create your models here.

class UploadedVideo(models.Model):
    name = models.CharField(max_length=100)
    size = models.IntegerField(null=True, blank= True)
    video_file = models.FileField(upload_to=u'shalent/static/uploaded_video')

