from django.forms import ModelForm
from shalent.models import UploadedVideo 

class VideoUploadForm(ModelForm):
    class Meta:
        model = UploadedVideo
        fields = ['name','video_file']
