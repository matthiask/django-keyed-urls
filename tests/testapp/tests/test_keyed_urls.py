from unittest import skipIf

import django
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import NoReverseMatch
from django.template import Context, Template, TemplateSyntaxError
from django.template.loader import render_to_string
from django.test import TestCase
from django.utils.translation import override

from keyed_urls import get_url, get_forwarding_url
from keyed_urls.models import KeyedURL


class KeyedURLTest(TestCase):
    def test_get_url(self):
        url = KeyedURL.objects.create(
            key='test1',
            url='https://example.com/test1',
        )

        self.assertEqual('%s' % url, 'test1')
        self.assertEqual(url.url, url.get_absolute_url())
        self.assertEqual(url.url, 'https://example.com/test1')

        self.assertEqual(get_url('test1'), 'https://example.com/test1')

        url.url = 'https://example.com/test2'
        url.save()

        with self.assertNumQueries(1):
            self.assertEqual(get_url('test1'), 'https://example.com/test2')
            self.assertEqual(get_url('test1'), 'https://example.com/test2')

        url.url_en = 'https://example.com/test-en'
        url.url_de = 'https://example.com/test-de'
        url.save()

        with self.assertNumQueries(2):
            self.assertEqual(
                get_url('test1', language='en'),
                'https://example.com/test-en')
            self.assertEqual(
                get_url('test1', language='de'),
                'https://example.com/test-de')

            self.assertEqual(
                get_url('test1', language=None),
                'https://example.com/test-en')

            with override('de'):
                self.assertEqual(
                    get_url('test1', language=None),
                    'https://example.com/test-de')

            with override('de-ch'):
                self.assertEqual(
                    get_url('test1', language=None),
                    'https://example.com/test-de')

            self.assertEqual(
                get_url('test1', language='de-ch'),
                'https://example.com/test-de')

        url.delete()
        with self.assertNumQueries(1):
            self.assertEqual(
                get_url('test1', language='en'),
                None)
            self.assertEqual(
                get_url('test1', language='de'),
                None)

            self.assertEqual(
                get_url('test1', language='en'),
                None)
            self.assertEqual(
                get_url('test1', language='de'),
                None)

    def test_templatetag(self):
        KeyedURL.objects.create(
            key='test1',
            url_de='german',
            url_en='english',
        )

        with override('en'):
            html = render_to_string('test.html')

        self.assertIn(
            'test1:english#',
            html)
        self.assertIn(
            'test1:en:english#',
            html)
        self.assertIn(
            'test1:de:german#',
            html)
        self.assertIn(
            'test1:fr:english#',
            html)
        self.assertIn(
            'test1:it:var:english#',
            html)

    def test_templatetag_failures(self):
        self.assertRaises(
            TemplateSyntaxError,
            Template,
            '{% load keyed_urls %} {% keyed_url %}',
        )

        self.assertRaises(
            TemplateSyntaxError,
            Template,
            '{% load keyed_urls %} {% keyed_url "test1" bla-=3 %}',
        )

        template = Template(
            '{% load keyed_urls %}{% keyed_url "invalid key" %}')
        # The template just shows "None"
        self.assertEqual(
            template.render(Context({})),
            u'None',
        )

        template = Template(
            '{% load keyed_urls %}{% keyed_url "invalid key" as var %}'
            '{{ var|default:"-" }}')
        self.assertEqual(
            template.render(Context({})),
            u'-',
        )

    def test_forwarders(self):
        key = KeyedURL.objects.create(
            key='test1',
            url_en='http://testserver/whatever-en',
            url_de='http://testserver/whatever-de',
        )

        with override('de'):
            self.assertEqual(
                key.get_forwarding_url(),
                '/de/ku/forward/test1/',
            )
            self.assertEqual(
                get_forwarding_url('test1'),
                '/de/ku/forward/test1/',
            )
            self.assertEqual(
                get_forwarding_url('test1', language='en'),
                '/en/ku/forward/test1/',
            )
            self.assertEqual(
                get_forwarding_url('test1'),
                '/de/ku/forward/test1/',
            )

        with override('it'):
            self.assertEqual(
                key.get_forwarding_url(),
                '/it/ku/forward/test1/',
            )

        self.assertRedirects(
            self.client.get('/en/ku/forward/test1/'),
            'http://testserver/whatever-en',
            target_status_code=404,
        )

    def test_invalid_keys(self):
        key = KeyedURL.objects.create(
            key='invalid with spaces',
            url='http://testserver/whatever',
        )

        self.assertRaises(
            NoReverseMatch,
            key.get_forwarding_url,
        )

        self.assertRaises(
            NoReverseMatch,
            get_forwarding_url,
            'invalid with spaces',
        )

    def test_admin_validation(self):
        User.objects.create_superuser(
            'admin', 'admin@example.com', 'password')

        self.client.login(username='admin', password='password')

        response = self.client.post(
            '/admin/keyed_urls/keyedurl/add/',
            {
                'key': 'invalid with spaces',
            }
        )

        self.assertRegexpMatches(
            response.content.decode('utf-8'),
            r'Enter a valid.+slug.+consisting of letters,',
        )

    @skipIf(
        django.VERSION < (1, 6),
        'This test requires Django 1.6 or better.',
    )
    def test_django16_model_validation(self):
        key = KeyedURL.objects.create(
            key='invalid with spaces',
            url='http://testserver/whatever',
        )

        try:
            key.full_clean()
        except ValidationError as exc:
            self.assertIn(
                'Enter a valid \'slug\'',
                str(exc),
            )
        else:
            self.fail('ValidationError not raised')  # noqa
