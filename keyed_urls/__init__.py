VERSION = (0, 4, 1)
__version__ = '.'.join(map(str, VERSION))


_none_type = 0xc0ffee
_available_languages = None


class KeyDoesNotExist(Exception):
    pass


def get_url(key, language=None, fail_silently=False):
    global _available_languages

    from django.conf import settings
    from django.core.cache import cache
    from django.utils.translation import get_language, override
    from keyed_urls.models import KeyedURL

    if _available_languages is None:
        _available_languages = [row[0] for row in settings.LANGUAGES]

    language = language if language is not None else get_language()

    # Django 1.6 comes with trans_real.get_supported_language_variant;
    # earlier versions do not. We are being fast and cheap here.
    if language not in _available_languages:
        language = language.split('-')[0]

    cache_key = 'keyed_urls:%s:%s' % (key, language)

    url = cache.get(cache_key)

    if url is None:
        try:
            instance = KeyedURL.objects.get(key=key)
        except KeyedURL.DoesNotExist:
            # We can be smart here and initialize the cache for all
            # languages.
            cache.set_many(dict((
                'keyed_urls:%s:%s' % (key, language),
                _none_type,
                ) for language, _ in settings.LANGUAGES
            ))
            url = None

        else:
            with override(language=language):
                url = instance.url

            cache.set(cache_key, _none_type if url is None else url, 120)

    if url == _none_type:
        url = None

    if url is None and not fail_silently:
        raise KeyDoesNotExist('No match found for key "%s".' % key)

    return None if url == _none_type else url


def get_forwarding_url(key, language=None):
    from django.core.urlresolvers import reverse
    from django.utils.translation import override

    if language is None:
        return reverse('keyed_url_forward', kwargs={'key': key})
    with override(language):
        return reverse('keyed_url_forward', kwargs={'key': key})
