import re
import random
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from steam.models import Profile,Match,Vote,Responses, RequestFriendship, Friendship
from django.contrib.auth import login as user_login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms.models import ModelForm, inlineformset_factory
from django.forms.models import ModelForm, inlineformset_factory
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from steam.forms import RegistrationForm
from datetime import datetime, date, time
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
    user = request.user
    profile = Profile.objects.get(user=user)

    user_preference = profile.preference
    user_gender = profile.gender

    potentials = []

    # Find all potential matches that this user hasn't yet seen
    for p in Profile.objects.all():
        already_friends = False
        for f in Friendship.objects.all():
            if (f.friend1 == p and f.friend2 == profile) or (f.friend1 == profile and f.friend2 == p):
                already_friends = True

        for f in RequestFriendship.objects.all():
            if (f.initiator == p and f.friended == profile) or (f.initiator == profile and f.friended == p):
                already_friends = True

        else:
            if already_friends == False and (p != profile):
                potentials.append(p)

    msg = ""
    msg_exists = False
    lucky_one = ""

    # If nobody to match throw an error
    if len(potentials) == 0:
        msg = "There are no other suggested friends for you right now!"
        msg_exists = True

    # Randomly generate one of these for display
    if len(potentials) > 0:
        lucky_one = random.choice(potentials)

    # Generate list of all friend requests

    my_requests = RequestFriendship.objects.filter(initiator=profile)

    requested_me = RequestFriendship.objects.filter(friended=profile)

    print requested_me

    return render_to_response('steam/friendrequests.html',
        {'lucky_one':lucky_one, 'profile':profile,'my_requests':my_requests, 'requested_me':requested_me, 'msg':msg, 'msg_exists':msg_exists},
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

def process_like(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        match_id = request.POST.get('profile')
        associated_user = User.objects.get(id=match_id)
        other_user = Profile.objects.get(user=associated_user)
        
        time = datetime.now()

        new_rf = RequestFriendship(initiator=profile,
            friended=other_user,
            accepted="F",
            time_requested = time,
            time_response = time,
            )

        new_rf.save()

        return redirect('/steam/friendrequests')


def process_friend_accept(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    initiator_id = request.POST.get('profile')
    request_id = request.POST.get('request')
    user_associated = User.objects.get(id=initiator_id)
    initiator = Profile.objects.get(user=user_associated)

    new_friendship = Friendship(
        friend1=profile,
        friend2=initiator)

    new_friendship.save()

    request = RequestFriendship.objects.get(id=int(request_id))

    request.accepted = 'T'
    request.time_response = datetime.now()

    request.save()

    return redirect('/steam/friendrequests')

def process_friend_reject(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    initiator_id = request.POST.get('profile')
    request_id = request.POST.get('request')
    user_associated = User.objects.get(id=initiator_id)
    initiator = Profile.objects.get(user=user_associated)
    
    request = RequestFriendship.objects.get(id=int(request_id))

    request.accepted = 'T'
    request.time_response = datetime.now()

    request.save()

    return redirect('/steam/friendrequests')

def matches(request):
    # if request.method == 'POST':
    #     form = MatchesForm(request.POST)
    #     if form.is_valid():
    #         print form.cleaned_data
    #         # form.save()
    #         return HttpResponseRedirect(reverse(('steam.views.home')))
    # else:
    #     form = MatchesForm()
    return render_to_response('steam/matches.html',
        {},
        context_instance=RequestContext(request))
    # matches_for_user_1 = Match.objects.filter(user1=1)
    # matches_for_user_2 = Match.objects.filter(user2=1)
    # final_matches_1 = []
    # final_matches_2 = []
    # for m in matches_for_user_1:
    #     num_votes = Vote.objects.filter(match=m).filter(y_or_n='y').count()
    #     if (num_votes >= VOTES_THRESHOLD):
    #         final_matches_1.append(m)
    # for m in matches_for_user_2:
    #     num_votes = Vote.objects.filter(match=m).filter(y_or_n='y').count()
    #     if (num_votes >= VOTES_THRESHOLD):
    #         final_matches_2.append(m)
        
    # return render_to_response('steam/matches.html',
    #     { 'final_matches_1' : final_matches_1,
    #     'final_matches_2' : final_matches_2},

    
    #     context_instance=RequestContext(request))

def go(request):
    # print "hello"
    # print request
    print "accept1"
    print request.POST.get("accept1", "")
    return render_to_response('steam/matches.html',{ },context_instance=RequestContext(request))
