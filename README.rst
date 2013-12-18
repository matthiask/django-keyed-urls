=================
django-keyed-urls
=================

.. image:: https://travis-ci.org/matthiask/django-keyed-urls.png?branch=master
   :target: https://travis-ci.org/matthiask/django-keyed-urls

An app for those cases when you want database-configurable URLs.


Installation
------------

Install ``django-keyed-urls`` with pip::

    pip install django-keyed-urls

Add ``keyed_urls`` and ``modeltranslation`` to ``INSTALLED_APPS``.

Specify a custom location for South migrations for ``keyed_urls`` -- you really
want to use South to handle schema changes when adding or removing languages
from ``LANGUAGES``::

    SOUTH_MIGRATION_MODULES = {
        'keyed_urls': 'yourapp.migrate.keyed_urls',
    }

Create and run database migrations::

    python manage.py schemamigration keyed_urls --initial
    python manage.py migrate keyed_urls


If you want to use the forwarding URLs, add an entry to your URLconf file. It
is recommended to use ``i18n_patterns`` because that means that
language-specific redirection URLs are automatically handled correctly::

    from django.conf.urls import include, url
    from django.conf.urls.i18n import i18n_patterns

    urlpatterns += i18n_patterns(
        '',
        url(r'', include('keyed_urls.urls'),
    )


Usage
-----

Template tags
~~~~~~~~~~~~~

Usage is simple::

    {% load keyed_urls %}

    {% keyed_url 'some_key' as url %}

    <a href="{{ url }}">bla</a>

Or::

    {% load keyed_urls %}

    {% keyed_url 'some_key' language='en' as url %}

    <a href="{{ url }}">bla</a>


Helpers
~~~~~~~

TODO Describe ``keyed_urls.get_url`` and ``keyed_urls.get_forwarding_url``.
