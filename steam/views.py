import re
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from steam.models import Profile,Match,Vote,Responses, RequestFriendship
from django.contrib.auth import login as user_login
from django.contrib.auth import authenticate
from django.forms.models import ModelForm, inlineformset_factory
from django.forms.models import ModelForm, inlineformset_factory
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                user_login(request, user)
                return render_to_response('steam/login.html',
                {
                },
                context_instance=RequestContext(request))

            else:
                return HttpResponse("Your account has been disabled")

        else:
            return render_to_response('steam/login.html',
                {
                'exists_error':True,
                'error':"Please enter a valid username/password combination."
                },
                context_instance=RequestContext(request))


    return render_to_response('steam/login.html',
        {
        'error':False,
        },
       context_instance=RequestContext(request))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('steam.views.home'))

def home(request):
    return render_to_response('steam/home.html',
        { 'profiles' : Profile.objects.all().order_by('uid') },
        context_instance=RequestContext(request))
def friendrequests(request):
    friendrequests =RequestFriendship.objects.filter(initiator=1)
    return render_to_response('steam/friendrequests.html',
        { 'friendrequests' : friendrequests },
        context_instance=RequestContext(request))
   
def questions(request):
    past_questions = Responses.objects.filter(uid=1)
    return render_to_response('steam/questions.html',
        { 'past_questions' : past_questions},
        context_instance=RequestContext(request))
def vote(request):
    past_votes = Vote.objects.filter(uid=1)
    return render_to_response('steam/vote.html',
        { 'past_votes' : past_votes},
        context_instance=RequestContext(request))
def matches(request):
    matches_for_user_1 = Match.objects.filter(user1=1)
    matches_for_user_2 = Match.objects.filter(user2=1)
  
    return render_to_response('steam/matches.html',
        { 'matches_for_user_1' : matches_for_user_1,
        'matches_for_user_2':matches_for_user_2},
    
        context_instance=RequestContext(request))

