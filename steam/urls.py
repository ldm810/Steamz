from django.conf.urls import patterns, include, url

urlpatterns = patterns('steam.views',
    url(r'^$', 'home'),
    url(r'^home$', 'home', name='home'),
    url(r'^register$', 'register'),
    url(r'^friendrequests$', 'friendrequests', name='friendrequests'),
    url(r'^go$', 'go', name='go'),
    url(r'^questions$', 'questions', name='questions'),
    url(r'^answer$', 'answer', name='answer'),
    url(r'^vote$', 'vote', name='vote'),
    url(r'^matches$', 'matches', name='matches'),
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout')
 
)
