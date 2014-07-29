from httplib2 import Http
import logging
import oauth2 as oauth
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect, render_to_response
from Auth.models import UserProfile
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core import signing
# from forms import SignupForm, AuthenticateForm
import json
import urllib
import cgi
import settings


def logout_req(request):
    logout(request)
    return redirect('/')

def register(request):
    signup_form = SignupForm(data=request.POST)
    if request.method == 'POST':
        if  signup_form.is_valid():
            username = signup_form.clean_email()
            email = signup_form.cleaned_data['email']
            password =  signup_form.clean_password2()
            obj = UserProfile.objects.create_user(username,email,password)
            obj.save()
            user = authenticate(email=username, password=password)
            obj.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return HttpResponse('success')
        else:
            form = SignupForm()
    return render(request, 'signup.html',{'form':signup_form})


"""
Method for Login through Facebook
"""
def facebook_login(request):
    params = {
        'scope': settings.FACEBOOK_APP_SCOPE,
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': settings.SITE_URL + '/auth/facebook/callback'
    }
    url = "https://graph.facebook.com/oauth/authorize?" + urllib.urlencode(params)
    return HttpResponseRedirect(url)


"""
Facebook social auth callback method
"""
def facebook_login_callback(request):
    params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'redirect_uri': settings.SITE_URL + '/auth/facebook/callback',
        'code': request.GET['code'] if 'code' in request.GET else ''
    }
    if not params['code']:
        return render_to_response('home.jade', 
                                 {'message': 'Error while login through facebook'},
                                 context_instance=RequestContext(request))

    response = cgi.parse_qs(urllib.urlopen( "https://graph.facebook.com/oauth/access_token?" +\
                             urllib.urlencode(params)).read()) 
    access_token = response["access_token"][-1]
    user_profile = json.load(urllib.urlopen("https://graph.facebook.com/me?" + \
                        urllib.urlencode(dict(access_token=access_token))))
    if not 'email' in user_profile.keys():
        return render_to_response('home.jade', 
                                 {'message': 'Unable to fetch your facebook profile'},
                                 context_instance=RequestContext(request))
    custom_profile = {
        'first_name': user_profile['first_name'],
        'last_name': user_profile['last_name'],
        'username': user_profile['email'],
        'email': user_profile['email'],
        'source': 'facebook'
    }
    print 'Facebook Auth: ', custom_profile
    result = create_user_from_social_auth(request, custom_profile)
    print "result",result
    print result
    if result == True:
        return redirect('/index',{'custom_profile':custom_profile})
    elif result == False:
        return redirect('/new_user')
    else:
        return render_to_response('home.jade', 
                                 {'message': 'Error while creating User'},
                                 context_instance=RequestContext(request))   



"""
Method for Login through Google
"""
def google_login(request):
    token_request_uri = "https://accounts.google.com/o/oauth2/auth"
    response_type = "code"
    client_id = settings.GOOGLE_CLIENT_ID
    redirect_uri = request.build_absolute_uri('/auth/google/callback')
    scope = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
    url = "%s?response_type=%s&client_id=%s&redirect_uri=%s&scope=%s"%(\
            token_request_uri,response_type,client_id,redirect_uri,scope)
    return HttpResponseRedirect(url)


"""
Google oauth2 callback method
"""
def google_login_callback(request):
    parser = Http()
    login_failed_url = '/'
    if 'error' in request.GET or 'code' not in request.GET:
        return render_to_response('home.jade', 
                                 {'message': 'Error while logging through Google'},
                                 context_instance=RequestContext(request))
    access_token_uri = 'https://accounts.google.com/o/oauth2/token'
    redirect_uri = request.build_absolute_uri('/auth/google/callback')
    params = urllib.urlencode({
        'code': request.GET['code'],
        'redirect_uri': redirect_uri,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'grant_type': 'authorization_code'
    })
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    resp, content = parser.request(access_token_uri, method = 'POST', body = params, headers = headers)
    token_data = json.loads(content)
    resp, content = parser.request("https://www.googleapis.com/oauth2/v1/userinfo?access_token=" + token_data['access_token'])
    user_profile = json.loads(content)
    custom_profile = {
        'first_name': user_profile['given_name'],
        'last_name': user_profile['family_name'],
        'username': user_profile['email'],
        'email': user_profile['email'],
        'source': 'google'
    }
    result = create_user_from_social_auth(request, custom_profile)
    print result
    if result == True:
        return redirect('/index')
    elif result == False:
        return redirect('/new_user')
    else:
        return render_to_response('home.jade', 
                                 {'message': 'Error while creating User'},
                                 context_instance=RequestContext(request))   


"""
Method for creating User in UserProfile 
"""
def create_user_from_social_auth(request, user_profile):
    user = UserProfile.objects.filter(email = user_profile['email'])
    if len(user):
        print 'User found in db'
        user = user[0]
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return True 
    try:
        print 'Creating New User'
        user = UserProfile(**user_profile)
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return False
    except Exception, e:
        print 'Error while creating user: ', str(e)
        return False
