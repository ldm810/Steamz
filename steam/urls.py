from django.conf.urls import patterns, include, url

urlpatterns = patterns('steam.views',
    url(r'^$', 'home'),
    url(r'^home$', 'home', name='home'),
    url(r'^register$', 'register'),
    url(r'^friendrequests$', 'friendrequests', name='friendrequests'),
    url(r'^go$', 'go', name='go'),
    url(r'^questions$', 'questions', name='questions'),
    url(r'^vote$', 'vote', name='vote'),
    url(r'^matches$', 'matches', name='matches'),
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),
    url(r'^process_like$', 'process_like'),
    url(r'^process_friend_accept$', 'process_friend_accept'),
    url(r'^process_friend_reject$', 'process_friend_reject'),

)
