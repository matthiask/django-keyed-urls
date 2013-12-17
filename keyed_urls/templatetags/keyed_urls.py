from __future__ import absolute_import

from django import template
from django.template import TemplateSyntaxError
from django.template.defaulttags import kwarg_re
from django.utils.encoding import smart_str

from keyed_urls import get_url


register = template.Library()


class KeyedURLNode(template.Node):
    def __init__(self, key, args, kwargs, asvar):
        self.key = key
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([
            (smart_str(k, 'ascii'), v.resolve(context))
            for k, v in self.kwargs.items()])
        key = self.key.resolve(context)

        try:
            url = get_url(key, *args, **kwargs)
        except Exception:
            if self.asvar is None:
                raise
            url = ''

        if self.asvar:
            context[self.asvar] = url
            return u''
        else:
            return url


@register.tag
def keyed_url(parser, token):
    """
    Returns an URL for the key

    Also accepts additional arguments which are passed directly to
    ``keyed_url.get_url()``.

    Usage is simple::

        {% load keyed_urls %}
        {% keyed_url 'some_key' as url %}
        <a href="{{ url }}">bla</a>

    Or::

        {% load keyed_urls %}
        <a href="{% keyed_url 'some_key' language='en' as url %}">bla</a>
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError(
            "'%s' takes at least one argument" % bits[0])
    key = parser.compile_filter(bits[1])
    args = []
    kwargs = {}
    asvar = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError(
                    "Malformed arguments to keyed_url tag")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))

    return KeyedURLNode(key, args, kwargs, asvar)
