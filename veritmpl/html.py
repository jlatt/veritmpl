import functools
import re

from veritmpl import runtime


class HTMLEscape(object):
    tr_table = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        u'\u00BB': '&raquo;',
        u'\u00AB': '&laquo;',
        }

    entity_regex = re.compile('|'.join(map(re.escape, tr_table.iterkeys())), re.I)

    escape_sub = lambda self, m: self.tr_table[m.group(0)]

    def __call__(self, s):
        if self.entity_regex.search(s):
            return self.entity_regex.sub(self.escape_sub, s)
        else:
            return s

html_escape = HTMLEscape()


class HTML(runtime.Literal):
    """HTML is a Literal for HTML strings."""
    pass


class HTMLTemplate(runtime.Template):
    """HTMLTemplate is a Template that encodes strings as HTML
    during rendering.

    """
    def encode(self, value, out):
        if value is not None:
            encoded = html_escape(unicode(value))
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
        if isinstance(tuple, arg):
            attributes[arg[0]] = arg[1]
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
                buf.append('%s="%s"' % (key, html_escape(unicode(value))))
    return HTML(' '.join(buf) if buf else '')
