from django.shortcuts import render, render_to_response,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from shalent.forms import VideoUploadForm
from settings import FILE_UPLOAD_MAX_MEMORY_SIZE
from django.forms.util import ErrorList
from django.contrib.auth.decorators import login_required
from Auth.models import UserProfile,ArtCategory
import json
from shalent.models import UploadedVideo,UserProfile

# Create your views here.

def home(request):
    if request.user.is_anonymous():
        return render_to_response('home.jade', context_instance = RequestContext(request))
    return HttpResponseRedirect("/index")

def terms(request):
    return render_to_response("terms.jade")

@login_required
def index(request, *args, **kwargs):
    print 'kwrg',kwargs
    if request.method == 'POST':
        print request.POST
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

def new_user(request,*args,**kwargs):
    if request.method == 'POST':
        user = UserProfile.objects.get(id=request.user.id)
        user.user_type=request.POST['usercategory'] if 'usercategory' in request.POST else 'V'
        user.art_category_id = request.POST['category_type'] if 'usercategory' in request.POST and\
            request.POST['usercategory'] == 'A' else None
        user.save()
        return redirect('/index')
    category_types = list(ArtCategory.objects.all().values())
    return render(request,"new_user.html", {'art_category':category_types})

def get_category(request, *args, **kwargs):
    categories = list(ArtCategory.objects.all().order_by('category').values('id','category'))
    json_models = json.dumps(categories)
    return HttpResponse(json_models, mimetype="application/javascript")
