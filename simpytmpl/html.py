from cgi import escape as html_escape

from simpytmpl import runtime


class HTML(runtime.Literal):
    pass


class HTMLFilter(runtime.SimpleFilter):
    filter_type = HTML
    escape = html_escape


def attrs(*args, **kwargs):
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


def tag(name, *args, **kwargs):
    attributes = attrs(*args, **kwargs)
    if attributes:
        return HTML('<%s %s>' % (name, attributes))
    else:
        return HTML('<%s>' % name)
