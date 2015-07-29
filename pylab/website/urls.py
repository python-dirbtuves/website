from django.conf import settings
from django.conf.urls import url, include

from pylab.website import admin
from pylab.website import views

slug = r'[a-z0-9-]+'

urlpatterns = [
    url(r'^$', views.project_list, name='project-list'),
    url(r'^projects/create/$', views.project_create, name='create-project'),
    url(r'^projects/(?P<project_slug>%s)/$' % slug, views.project_details, name='project-details'),
    url(r'^projects/(?P<project_slug>%s)/update/$' % slug, views.project_update, name='project-update'),
    url(r'^events/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]+)/(?P<event_slug>%s)/$' % slug,
        views.event_details, name='event-details'),
    url(r'^about/$', views.about, name='about'),
]

urlpatterns += [
    url(r'^accounts/', include('pylab.accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
