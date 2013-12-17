=================
django-keyed-urls
=================

.. image:: https://travis-ci.org/matthiask/django-keyed-urls.png?branch=master
   :target: https://travis-ci.org/matthiask/django-keyed-urls

An app for those cases when you want database-configurable URLs.


Usage
-----

Usage is simple::

    {% load keyed_urls %}

    {% keyed_url 'some_key' as url %}

    <a href="{{ url }}">bla</a>

Or::

    {% load keyed_urls %}

    {% keyed_url 'some_key' language='en' as url %}

    <a href="{{ url }}">bla</a>
