import re
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from beers.models import Beer, Bar, Drinker, Frequents, Likes
from django.forms.models import ModelForm, inlineformset_factory
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

def login(request):
    return render_to_response('beers/login.html',
        {},
        context_instance=RequestContext(request))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('beers.views.all_drinkers'))

def all_drinkers(request):
    return render_to_response('beers/all-drinkers.html',
        { 'drinkers' : Drinker.objects.all().order_by('name') },
        context_instance=RequestContext(request))

def drinker(request, drinker_name):
    drinker = get_object_or_404(Drinker, pk=drinker_name)
    return render_to_response('beers/drinker.html',
        { 'drinker' : drinker, 
          # 'beers' : Beer.objects.raw('SELECT * FROM Beer WHERE name IN (SELECT beer FROM Likes WHERE drinker = %s) ORDER BY name', [drinker.name]),
          'beers' : Beer.objects.filter(likes__drinker__exact=drinker).order_by('name'),
          # 'frequents' : Frequents.objects.raw('SELECT * FROM Frequents WHERE drinker = %s ORDER BY bar', [drinker.name]),
          'frequents' : drinker.frequents_set.all().order_by('bar'),
        },
        context_instance=RequestContext(request))

class PartialDrinkerForm(ModelForm):
    class Meta:
        model = Drinker
        # Leave out name so it cannot be edited; at the same time, it means that
        # it won't be in the data submitted through the form either:
        exclude = ('name',)

@login_required(login_url=reverse_lazy('beers.views.login'))
def edit_drinker(request, drinker_name):
    drinker = get_object_or_404(Drinker, pk=drinker_name)
    LikesFormSet = inlineformset_factory(Drinker, Likes, extra=1)
    FrequentsFormSet = inlineformset_factory(Drinker, Frequents, extra=1) 
    return render_to_response('beers/edit-drinker.html',
        { 'drinker' : drinker,
          'drinkerForm' : PartialDrinkerForm(instance=drinker),
          'likesFormSet' : LikesFormSet(instance=drinker, prefix='BeersLiked'),
          'frequentsFormSet' : FrequentsFormSet(instance=drinker, prefix='BarsFrequented'),
        },
        context_instance=RequestContext(request))

def edit_drinker_submit(request, drinker_name):
    drinkerForm = PartialDrinkerForm(request.POST)
    # Remember to set drinker.name before updating the database, because
    # PartialDrinkerForm doesn't contain this information:
    drinker = drinkerForm.save(commit=False)
    drinker.name = drinker_name
    drinker.save()
    LikesFormSet = inlineformset_factory(Drinker, Likes)
    likesFormSet = LikesFormSet(request.POST, instance=drinker, prefix='BeersLiked')
    likesFormSet.save()
    FrequentsFormSet = inlineformset_factory(Drinker, Frequents)
    frequentsFormSet = FrequentsFormSet(request.POST, instance=drinker, prefix='BarsFrequented')
    frequentsFormSet.save()
    # Always return an HttpResponseRedirect after successfully dealing with
    # POST data.  This prevents data from being posted twice if a user hits
    # the back button.
    return HttpResponseRedirect(reverse('beers.views.drinker', args=(drinker.name,)))
