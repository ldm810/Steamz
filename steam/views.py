import re
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from steam.models import Profile,Match,Vote,Responses, RequestFriendship, Question
from django.contrib.auth import login as user_login
from django.contrib.auth import authenticate
from django.forms.models import ModelForm, inlineformset_factory
from django.forms.models import ModelForm, inlineformset_factory
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
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
    
    all_responses = Responses.objects.filter(user=request.user)

    all_questions = Question.objects.all()


    if len(all_responses) == 0:
        random_q = random.choice(all_questions)
    else:

        pick_question = True
        while pick_question:
        
            for response in all_responses:

                random_q =  random.choice(all_questions)   
                if random_q.qid == response.qid:
                    random_q = random.choice(all_questions)
                else:
                    pick_question = False

        



    return render_to_response('steam/questions.html',
        { 

        'past_questions': all_responses,
        'new_question': random_q


        },
        context_instance=RequestContext(request))

def answer(request):
    
    print "Response"
    y_or_n = request.POST.get("respond", "")
    question_id = request.POST.get("question", "")
    profile = Profile.objects.filter(user=request.user)[0]
    question = Question.objects.filter(qid=question_id)[0]
    response = Responses(user=profile, qid=question, answer=y_or_n)
    response.save()
    return render_to_response('steam/questions.html',{ },context_instance=RequestContext(request))


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