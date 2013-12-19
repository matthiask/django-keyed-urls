from django.conf.urls import include, patterns, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += i18n_patterns(
    '',
    url(r'^ku/', include('keyed_urls.urls')),
)
