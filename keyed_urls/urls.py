from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(
        r'^forward/(?P<key>[-a-zA-Z0-9_]+)/$',
        'keyed_urls.views.forward',
        name='keyed_url_forward',
    ),
)
