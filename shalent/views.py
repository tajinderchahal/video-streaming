from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from shalent.forms import VideoUploadForm
from settings import FILE_UPLOAD_MAX_MEMORY_SIZE
from django.forms.util import ErrorList
from django.contrib.auth.decorators import login_required
from Auth.models import UserProfile
from shalent.models import UploadedVideo

# Create your views here.

def home(request):
    print request.user
    if request.user.is_anonymous():
        return render_to_response('home.jade', 
                              context_instance = RequestContext(request))
    return HttpResponseRedirect("/index")

@login_required
def index(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if 'video_file' in request.FILES:
            is_video = request.FILES['video_file'].content_type.split('/')[0] == 'video' 
            if is_video:
                video_size = request.FILES['video_file']._size
                if video_size > FILE_UPLOAD_MAX_MEMORY_SIZE:
                    form.errors["video_file"] = ErrorList([u"File size cannot be more that 50 MB"])
            else:
                form.errors["video_file"] = ErrorList([u"File type is not supported"])
        if form.is_valid():
            user_profile = UserProfile.objects.get(id= request.user.id)
            uvideo = UploadedVideo(**{'user': user_profile,
                'name': form.cleaned_data['name'],
                'size': video_size,
                'video_file': form.cleaned_data['video_file']})
            uvideo.save()
            return render(request, 
                          'index.jade', 
                          {'form': form, 
                           'upload_status': 1 },
                            context_instance = RequestContext(request))
    else:
        form = VideoUploadForm()
    return render(request, 
                  'index.jade', 
                  {'form': form , 
                   'upload_status': 0},
                  context_instance = RequestContext(request))

