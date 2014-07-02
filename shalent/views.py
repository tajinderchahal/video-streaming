from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from shalent.forms import VideoUploadForm
from settings import FILE_UPLOAD_MAX_MEMORY_SIZE
from django.forms.util import ErrorList

# Create your views here.

def home(request):
    return render_to_response('home.jade', 
                              context_instance = RequestContext(request))

def index(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if 'video_file' in request.FILES:
            is_video = request.FILES['video_file'].content_type.split('/')[0] == 'video' 
            if is_video:
                if request.FILES['video_file']._size > FILE_UPLOAD_MAX_MEMORY_SIZE:
                    form.errors["video_file"] = ErrorList([u"File size cannot be more that 50 MB"])
            else:
                form.errors["video_file"] = ErrorList([u"File type is not supported"])
        if form.is_valid():
            upv = form.save()
            form = VideoUploadForm()
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

def index1(request):
    upload_status = request.GET['status'] if 'status' in request.GET else ''
    data_dict = {}
    if upload_status:
        upload_status['ups'] = 1
    return render_to_response('index.jade', data_dict,  
                              context_instance = RequestContext(request))
