from django.db import models
from Auth.models import UserProfile

class UploadedVideo(models.Model):
    user = models.ForeignKey(UserProfile)
    name = models.CharField(max_length=100)
    size = models.IntegerField(null=True, blank= True)
    file_type = models.CharField(max_length=50, null=True, blank=True)
    file_path = models.FileField((''), upload_to=u'shalent/static/uploaded_video')
