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
from steam.forms import RegistrationForm,MatchesForm

VOTES_THRESHOLD = 1


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

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(('steam.views.home')))
    else:
        form = RegistrationForm()
    return render_to_response('steam/register.html',
        { 'form': form, },
        context_instance=RequestContext(request))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('steam.views.home'))

def home(request):
    return render_to_response('steam/home.html',
        { },
        context_instance=RequestContext(request))

def friendrequests(request):
    # friendrequests =RequestFriendship.objects.filter(initiator=1)
    return render_to_response('steam/friendrequests.html',
        {},
        context_instance=RequestContext(request))
   
def questions(request):
    # past_questions = Responses.objects.filter(uid=1)
    return render_to_response('steam/questions.html',
        { },
        context_instance=RequestContext(request))

def vote(request):
    # past_votes = Vote.objects.filter(uid=1)
    return render_to_response('steam/vote.html',
        { },
        context_instance=RequestContext(request))
def matches(request):
    # if request.method == 'POST':
    #     form = MatchesForm(request.POST)
    #     if form.is_valid():
    #         print form.cleaned_data
    #         # form.save()
    #         return HttpResponseRedirect(reverse(('steam.views.home')))
    # else:
    #     form = MatchesForm()
    # return render_to_response('steam/matches.html',
    #     {},
    #     context_instance=RequestContext(request))
    matches_for_user_1 = Match.objects.filter(user1=request.user).exclude(accept1='y').exclude(accept1='n')
    matches_for_user_2 = Match.objects.filter(user2=request.user).exclude(accept2='y').exclude(accept2='n')
    print "matches",matches_for_user_1,matches_for_user_2
    final_matches_1 = []
    final_matches_2 = []
    # for m in matches_for_user_1:
    #     num_votes = Vote.objects.filter(match=m).filter(y_or_n='y').count()
    #     if (num_votes >= VOTES_THRESHOLD):
    #         final_matches_1.append(m)
    # for m in matches_for_user_2:
    #     num_votes = Vote.objects.filter(match=m).filter(y_or_n='y').count()
    #     if (num_votes >= VOTES_THRESHOLD):
    #         final_matches_2.append(m)
        
    return render_to_response('steam/matches.html',
        { 'final_matches_1' : matches_for_user_1,
        'final_matches_2' : matches_for_user_2},
        context_instance=RequestContext(request))

def go(request):

    response = request.POST.get("accept1", "")
    matchID = request.POST.get("match", "")
    userPos = request.POST.get("userPos", "")
    
    if (userPos == "1" ):
        match = Match.objects.filter(id=matchID).update(accept1=response)
    if (userPos=="2"):
        match = Match.objects.filter(id=matchID).update(accept2=response)
      
    return render_to_response('steam/matches.html',{ },context_instance=RequestContext(request))