class Template(object):
    EXHAUST_BYTES = 1024 * 1024

    def __init__(self, **kwargs):
        self.env = kwargs

    def __str__(self):
        return str(self.stringify())

    def __unicode__(self):
        return self.stringify()

    def __call__(self, out):
        return self.render(out)

    def render(self, out):
        raise NotImplementedError('%s.render' % self.__class__.__name__)

    def stringify(self):
        from StringIO import StringIO
        out = StringIO()
        self.render(out)
        return out.getvalue()

    output_encode = unicode

    def encode(self, value, out):
        if value is not None:
            encoded = self.output_encode(value)
            if value:
                out.write(encoded)

    def substitute(self, name, out):
        value = self.env.get(name)

        if isinstance(value, Template):
            value.render(out)
        elif hasattr(value, 'read') and callable(value.read): # TODO better file test?
            self.encode(value.read(), out)
        else:
            self.encode(value, out)

        return self


class Literal(unicode):
    def __new__(cls, s=u'', *args, **kwargs):
        return s if isinstance(s, cls) else super(Literal, cls).__new__(s, *args, **kwargs)
