from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from keyed_urls.models import KeyedURL


def forward(request, redirect_class=HttpResponseRedirect, **kwargs):
    url = get_object_or_404(KeyedURL, **kwargs)
    return redirect_class(url.url)
