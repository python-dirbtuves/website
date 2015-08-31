from django.conf import settings
from django.conf.urls import url, include

from pylab.website import admin
from pylab.website import views

slug = r'[a-z0-9-]+'
event = r'(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>%s)' % slug

urlpatterns = [
    url(r'^$', views.project_list, name='project-list'),
    url(r'^projects/create/$', views.project_create, name='create-project'),
    url(r'^projects/(?P<project_slug>%s)/$' % slug, views.project_details, name='project-details'),
    url(r'^projects/(?P<project_slug>%s)/update/$' % slug, views.project_update, name='project-update'),
    url(r'^events/%s/$' % event, views.event_details, name='event-details'),
    url(r'^events/%s/create-next-weekly-event/$' % event, views.create_weekly_event, name='create-weekly-event'),
    url(r'^about/$', views.about, name='about'),
    url(r'^vote/(?P<voting_poll_slug>%s)/$' % slug, views.voting_page, name='voting-page'),
    url(r'^voting-poll/(?P<voting_poll_slug>%s)/$' % slug, views.voting_poll_details, name='voting-poll-details'),
    url(r'^voting-poll-list', views.voting_poll_list, name='voting-poll-list'),
]

urlpatterns += [
    url(r'^accounts/', include('pylab.accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django_comments.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
