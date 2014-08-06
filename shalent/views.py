from django.shortcuts import render, render_to_response,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from shalent.forms import VideoUploadForm
from settings import FILE_UPLOAD_VIDEO_SIZE, FILE_UPLOAD_IMAGE_SIZE
from django.forms.util import ErrorList
from django.contrib.auth.decorators import login_required
from Auth.models import UserProfile,ArtCategory
import json
from shalent.models import UploadedVideo,UserProfile
from Auth.models import RendezvousUser

# Create your views here.

def home(request):
    if request.user.is_anonymous():
        return render_to_response('home.jade', context_instance = RequestContext(request))
    return HttpResponseRedirect("/index")

def terms(request):
    return render_to_response("terms.jade")

"""
Method for uploading video and 
"""
@login_required
def index(request):
    code = rendezvous_user(request)  # creating rendezvous entry
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if 'file_path' in request.FILES:
            file_type = request.FILES['file_path'].content_type.split('/')[0]
            file_size = request.FILES['file_path']._size
            if file_type == 'video':
                if file_size > FILE_UPLOAD_VIDEO_SIZE:
                    form.errors["file_path"] = ErrorList([u"File size cannot be more that 50 MB"])
            elif file_type == 'image':
                if file_size > FILE_UPLOAD_IMAGE_SIZE:
                    form.errors["file_path"] = ErrorList([u"File size cannot be more that 5 MB"])
            else:
                form.errors["file_path"] = ErrorList([u"File type is not supported (only Image and Video)"])

        if form.is_valid():
            user_profile = UserProfile.objects.get(id= request.user.id)
            uvideo = UploadedVideo(**{'user': user_profile,
                'name': form.cleaned_data['name'],
                'size': file_size,
                'file_type': file_type,
                'file_path': form.cleaned_data['file_path']})
            uvideo.save()
            return render(request, 
                          'index.jade',
                          {'form': form,
                           'code': code,
                           'upload_status': 1 },
                            context_instance = RequestContext(request))
    else:
        form = VideoUploadForm()

    return render(request, 
                  'index.jade',
                  {'form': form,
                   'code': code,
                   'upload_status': 0},
                  context_instance = RequestContext(request))


@login_required
def rendezvous_user(request):
    rend_user = RendezvousUser.objects.filter(user_profile_id = request.user.id)
    code = 0
    if not len(rend_user):
        if 'code' in request.POST:
            code = request.POST.get('code')
            obj = RendezvousUser()
            obj.user_profile_id = request.user.id
            obj.user_code = code
            obj.save()
    else:
        if 'code' in request.POST:
            rend_user[0].user_code = request.POST.get('code')
            rend_user[0].save()
            code = request.POST.get('code')
        else:
            code = rend_user[0].user_code
    return code


def new_user(request):
    if request.method == 'POST':
        user = UserProfile.objects.get(id=request.user.id)
        user.user_type = request.POST['usercategory'] \
            if 'usercategory' in request.POST else 'V'
        user.art_category_id = request.POST['category_type'] \
            if 'usercategory' in request.POST and \
                request.POST['usercategory'] == 'A' else None
        user.save()
        return redirect('/index')
    category_types = list(ArtCategory.objects.all().values())
    return render(request,
                  "new_user.jade", 
                  {'art_category': category_types}, 
                  context_instance = RequestContext(request))


def get_category(request):
    categories = list(ArtCategory.objects.all().order_by('category').values('id','category'))
    json_models = json.dumps(categories)
    return HttpResponse(json_models, mimetype="application/javascript")
