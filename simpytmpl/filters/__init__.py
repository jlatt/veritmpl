class Literal(unicode):
    def __new__(cls, s=u'', *args, **kwargs):
        return s if isinstance(s, cls) else super(Literal, cls).__new__(s, *args, **kwargs)


class SimpleFilter(object):
    filter_type = unicode

    escape = lambda self, value: value

    def __call__(self, value, out):
        out.write(value if isinstance(value, self.filter_type) else self.escape(value))

