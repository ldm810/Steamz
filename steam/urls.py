from django.conf.urls import patterns, include, url

urlpatterns = patterns('steam.views',
    url(r'^$', 'all_drinkers'),
    url(r'^all-drinkers$', 'all_drinkers', name='all_drinkers'),
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),
    url(r'^drinker/(?P<drinker_name>[^/]+)$', 'drinker'),
    url(r'^edit-drinker/(?P<drinker_name>[^/]+)$', 'edit_drinker'),
    url(r'^edit-drinker-submit/(?P<drinker_name>[^/]+)$', 'edit_drinker_submit'),
)
