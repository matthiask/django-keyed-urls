from django.conf.urls import patterns, url


urlpatterns = patterns(
    'keyed_urls.views',
    url(
        r'^forward/(?P<pk>\d+)/',
        'forward',
        name='keyed_url_forward_by_pk',
    ),
    url(
        r'^forward/(?P<key>[^/]+)/$',
        'forward',
        name='keyed_url_forward_by_key',
    ),
)
