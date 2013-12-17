VERSION = (0, 1, 0)
__version__ = '.'.join(map(str, VERSION))


_none_type = 0xc0ffee


def get_url(key, language=None):
    from django.conf import settings
    from django.core.cache import cache
    from django.utils.translation import get_language, override, trans_real
    from keyed_urls.models import KeyedURL

    language = language if language is not None else get_language()
    language = trans_real.get_supported_language_variant(language)
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
            if language:
                with override(language=language):
                    url = instance.url
            else:
                url = instance.url

            cache.set(cache_key, _none_type if url is None else url, 120)

    return None if url == _none_type else url
