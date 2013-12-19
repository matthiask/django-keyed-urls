=================
django-keyed-urls
=================

.. image:: https://travis-ci.org/matthiask/django-keyed-urls.png?branch=master
   :target: https://travis-ci.org/matthiask/django-keyed-urls

An app for those cases when you need language-specific URLs in the database
for use in templates or as redirects.


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

    <a href="{% keyed_url 'some_other_key' %}">bla</a>

Or::

    {% load keyed_urls %}

    {% keyed_url 'some_key' language='en' as url %}

    <a href="{{ url }}">bla</a>


If a key does not exist and the tag is used as an assignment tag, the variable
is set to ``None``. Otherwise, a  ``KeyDoesNotExist`` exception is raised which
also aborts template rendering. The behavior is equal to the behavior of
Django's own ``{% url %}`` template tag in this regard.


Helpers
~~~~~~~

Two additional helpers are available. If you need URLs in python code,
use the following snippet::

    from keyed_urls import get_url

    some_url = get_url('some_key')
    some_other_url = get_url('some_key', language='en')

The advantage of using ``get_url`` compared to fetching a ``KeyedURL`` model
from the database and accessing its ``url`` attribute is that ``get_url`` is
caching all results. Since ``get_url`` is also used internally by the template
tag described above this means that you do not have to worry about performance
as much as when using models directly. ``get_url`` raises a ``KeyDoesNotExist``
exception if a particular URL cannot be found. This can be prevented by passing
``fail_silently=True``.

The following snippet can be used to fetch the forwarding URL::

    from keyed_urls import get_forwarding_url

    url = get_forwarding_url('some_key')
    url = get_forwarding_url('some_key', language='de')

``get_forwarding_url`` is nothing more but a thin wrapper around Django's own
``reverse`` method. This method raises a ``NoReverseMatch`` exception if the
key is invalid, but does not check whether the given key exists at all in the
database. When visiting the link, users will get a 404 response. For
``get_forwarding_url`` to work you have to include ``keyed_urls.urls``
somewhere in your URLconf as described above, preferrably inside an
``i18n_patterns`` block.
