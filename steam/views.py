import re
import random
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext

from django.shortcuts import render_to_response, get_object_or_404, redirect
from steam.models import Profile,Match,Vote,Responses, Question, RequestFriendship, Friendship

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

import random

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

@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('steam.views.home'))

def home(request):
    return render_to_response('steam/home.html',
        { },
        context_instance=RequestContext(request))

@login_required
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
   
@login_required
def questions(request):
    
    current_user = request.user
    print current_user.first_name
    print "?????"

    all_responses = Responses.objects.filter(user=request.user)
    for r in all_responses:
        print r.qid.question_text

    all_questions = Question.objects.all()

    random_q = random.choice(all_questions)

    msg = ""
    msg_exists = False

    if len(all_responses) == len(all_questions):
        msg = "You have no more questions to answer!"
        msg_exists = True


    if len(all_responses) == 0:
        random_q = random.choice(all_questions)
    else:
        count = 0
        response_IDs = []
        for response in all_responses:
            response_IDs.append(response.qid.qid)
        get_question = True
        while get_question:
            count += 1
            print count
            random_q = random.choice(all_questions) 
            test_qid = random_q.qid
            if test_qid not in response_IDs:
                get_question = False

            if len(all_responses) == len(all_questions):

                get_question = False
            


    return render_to_response('steam/questions.html',
        { 

        'past_questions': all_responses,
        'new_question': random_q,
        'msg':msg, 
        'msg_exists':msg_exists


        },
        context_instance=RequestContext(request))

@login_required
def answer(request):
    
    print "Response"
    y_or_n = request.POST.get("respond", "")
    question_id = request.POST.get("question", "")
    profile = Profile.objects.filter(user=request.user)[0]
    question = Question.objects.filter(qid=question_id)[0]
    response = Responses(user=profile, qid=question, answer=y_or_n)
    response.save()

    return redirect('questions')

    #return redirect('steam/questions.html', {}, context_instance=RequestContext(request))


@login_required
def vote(request):
    # potential_votes = Vote.objects.filter(uid=1)
    person = Profile.objects.filter(user=request.user)
    previous_votes = Vote.objects.filter(uid=person)
    matches = Match.objects.exclude(user1=request.user).exclude(user2=request.user)
    matchToVoteOn = []
    user1Questions = []
    user2Questions = []
    no_matches = False
    user1NoResponses = False
    user2NoResponses = False
    no_previous_votes  = False
    for m in matches:
       
        votes = Vote.objects.filter(match=m).filter(uid=person)
        friends =[]
        friends.extend(Friendship.objects.filter(friend1=person).filter(friend2=m.user1))
        friends.extend(Friendship.objects.filter(friend2=person).filter(friend1=m.user1))

        friends.extend(Friendship.objects.filter(friend1=person).filter(friend2=m.user2))
        friends.extend(Friendship.objects.filter(friend2=person).filter(friend1=m.user2))
        print "friends",friends
        if (len(votes) == 0 and len(friends) !=0):
            matchToVoteOn.append(m)
            print 'match to vote on ' , m
            break 
    if (len(matchToVoteOn)!=0):
        user1Questions = Responses.objects.filter(user=matchToVoteOn[0].user1)
        user2Questions = Responses.objects.filter(user=matchToVoteOn[0].user2)
        if (len(user1Questions) == 0):
            user1NoResponses = True
        if (len(user2Questions)==0):
            user2NoResponses = True
    else:
        no_matches = True
    if (len(previous_votes) == 0):
        no_previous_votes = True
    return render_to_response('steam/vote.html',
        { 'match': matchToVoteOn, 'previous_votes':previous_votes, 
        'user1Questions':user1Questions,'user2Questions':user2Questions, 
        'no_matches' : no_matches,'no_previous_votes':no_previous_votes,
        'user1NoResponses':user1NoResponses,'user2NoResponses':user2NoResponses},
        context_instance=RequestContext(request))

@login_required
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

@login_required
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

@login_required
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

@login_required
def matches(request):

    matches_for_user_1 = Match.objects.filter(user1=request.user).exclude(accept1='y').exclude(accept1='n')
    matches_for_user_2 = Match.objects.filter(user2=request.user).exclude(accept2='y').exclude(accept2='n')
    print "matches",matches_for_user_1,matches_for_user_2
    final_matches_1 = []
    final_matches_2 = []
    no_accepts = False
    no_matches = False
    for m in matches_for_user_1:
        num_votes = Vote.objects.filter(match=m).filter(y_or_n='y').count()
        if (num_votes >= VOTES_THRESHOLD):
            final_matches_1.append(m)
    for m in matches_for_user_2:
        num_votes = Vote.objects.filter(match=m).filter(y_or_n='y').count()
        if (num_votes >= VOTES_THRESHOLD):
            final_matches_2.append(m)
        
    accepted_for_user_1 = Match.objects.filter(user1=request.user).filter(accept1='y').filter(accept1='y')
    accepted_for_user_2 = Match.objects.filter(user2=request.user).filter(accept2='y').filter(accept2='y')
    if (len(accepted_for_user_2) == 0 and len(accepted_for_user_1)==0):
        no_accepts = True
    if (len(final_matches_1) == 0 and len(final_matches_2)==0):
        no_matches = True
    return render_to_response('steam/matches.html',
        { 'final_matches_1' : final_matches_1,
        'final_matches_2' : final_matches_2,
        'accepted_for_user_1':accepted_for_user_1,
        'accepted_for_user_2':accepted_for_user_2,
        'no_accepts':no_accepts,
        'no_matches':no_matches},
        context_instance=RequestContext(request))

@login_required
def friends(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    all_friends = Friendship.objects.filter(friend1=profile)
    all_friends2 = Friendship.objects.filter(friend2=profile)

    friendless = False
    if len(all_friends) == 0 and len(all_friends2) == 0:
        friendless= True

    return render_to_response(
        'steam/friends.html', {'friendless':friendless, 'all_friends':all_friends, 'all_friends2':all_friends2},RequestContext(request))

@login_required
def remove_friend(request):
    user = request.user
    friendship_id = request.POST.get('friendship')
    friendship = Friendship.objects.get(id=friendship_id)
    friendship.delete()

    return redirect('/steam/friends')

@login_required
def go(request):


    response = request.POST.get("accept1", "")
    matchID = request.POST.get("match", "")
    userPos = request.POST.get("userPos", "")
    
    if (userPos == "1" ):
        match = Match.objects.filter(id=matchID).update(accept1=response)
    if (userPos=="2"):
        match = Match.objects.filter(id=matchID).update(accept2=response)
      
    return render_to_response('steam/matches.html',{ },context_instance=RequestContext(request))

@login_required
def vote_on_match(request):

   
    matchID = request.POST.get("match", "")
    vote = request.POST.get("vote", "")
    uid = Profile.objects.filter(user=request.user)[0]
    match = Match.objects.filter(id=matchID)[0]
    new_vote = Vote(y_or_n=vote,match=match,uid=uid)
    new_vote.save()
    print 'new_vote',new_vote
      
    return render_to_response('steam/vote.html',{ },context_instance=RequestContext(request))

@login_required
def suggest_friends(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    
    my_friends_list = find_my_friends(profile)

    possible_friends = []
    
    for f in my_friends_list:
        f_friends_list = find_my_friends(f)
        if f not in my_friends_list:
            possible_friends.append(f)

    msg = ""

    if len(possible_friends) == 0:
        msg = "We couldn't find any friends to match you with."

    return render_to_response(
        "steam/suggest_friends.html",
        {'possible_friends':possible_friends, 'msg':msg},
        context_instance=RequestContext(request))

@login_required
def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    
    my_friends_list = find_my_friends(profile)

    return render_to_response(
        "steam/profile.html",
        {'profile':profile, 'friends':my_friends_list},
        context_instance=RequestContext(request))


def find_my_friends(profile):
    f1 = Friendship.objects.filter(friend1=profile)
    f2 = Friendship.objects.filter(friend2=profile)

    friends_list = []

    for f in f1:
        friend_to_add = f1.friend2
        friends_list.append(friend_to_add)

    for f in f2:
        friend_to_add = f2.friend1
        friends_list.append(friend_to_add)

    return friends_list
