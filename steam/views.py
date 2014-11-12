import re
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from steam.models import Profile,Match,Vote
# , Personality, Question,Responses
from django.forms.models import ModelForm, inlineformset_factory
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

def login(request):
    return render_to_response('steam/login.html',
        {},
        context_instance=RequestContext(request))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('steam.views.home'))

def home(request):
    return render_to_response('steam/home.html',
        { 'profiles' : Profile.objects.all().order_by('uid') },
        context_instance=RequestContext(request))
    # return render_to_response('steam/home.html',
    #     context_instance=RequestContext(request))
def questions(request):
    return render_to_response('steam/questions.html',
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

    # return render_to_response('steam/matches.html',
    #     context_instance=RequestContext(request))
 

