from django.template.loader import render_to_string
from django.test import TestCase
from django.utils.translation import override

from keyed_urls import get_url
from keyed_urls.models import KeyedURL


class KeyedURLTest(TestCase):
    def test_get_url(self):
        url = KeyedURL.objects.create(
            key='test1',
            url='https://example.com/test1',
        )

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
