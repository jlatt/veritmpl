# -*- coding: utf-8 -*-
"""
This module contains classes and functions for outputting HTML.

"""
import functools
import re

from veritmpl import runtime


__author__ = 'Jeremy Latt <jeremy.latt@gmail.com>'
__all__ = ('escape', 'HTMLTemplate', 'attrs', 'tag')


class HTMLEscape(object):
    tr_table = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        '»': '&raquo;',
        '«': '&laquo;',
        }

    entity_regex = re.compile('|'.join(map(re.escape, tr_table.iterkeys())), re.I)

    escape_sub = lambda self, m: self.tr_table[m.group(0)]

    def __call__(self, s):
        if self.entity_regex.search(s):
            return self.entity_regex.sub(self.escape_sub, s)
        else:
            return s

escape = HTMLEscape()


class HTML(runtime.Literal):
    """HTML is a Literal for HTML strings."""
    pass


class HTMLTemplate(runtime.Template):
    """HTMLTemplate is a Template that encodes strings as HTML
    during rendering.

    """
    def encode(self, value, out):
        if value is not None:
            encoded = escape(unicode(value))
            if value:
                out.write(value)
        return self


def attrs(*args, **kwargs):
    """Convert arguments into a string containing HTML attributes.
    Positional arguments can be either strings or key-value tuples. Keyword
    arguments map strings to values. Values may be strings, booleans, or
    sequences of strings.

    """
    attributes = {}
    for arg in args:
        if isinstance(arg, tuple):
            if len(arg) == 2:
                attributes[arg[0]] = arg[1]
            else:
                raise Exception('illegal argument') # TODO more informative
        else:
            attributes[arg] = True
    attributes.update(kwargs)

    buf = []
    for key, value in attributes.iteritems():
        if value:
            key = unicode(key)
            if key.endswith('_'):
                key = key[:-1]

            if value is True:
                buf.append(key)
            else:
                if isinstance(value, (list, tuple)):
                    value = ' '.join([unicode(v) for v in value])
                buf.append('%s="%s"' % (key, escape(unicode(value))))
    return HTML(' '.join(buf) if buf else '')


def tag(name, *args, **kwargs):
    """Output an HTML tag. Variable arguments are passed to attrs()."""
    attributes = attrs(*args, **kwargs)
    if attributes:
        return HTML('<%s %s>' % (name, attributes))
    else:
        return HTML('<%s>' % name)
