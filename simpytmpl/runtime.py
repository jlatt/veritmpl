class Template(object):

    def filter(self, value, out):
        out.write(value)

    def __init__(self, **kwargs):
        self.env = kwargs

    def __str__(self):
        return str(self.stringify())

    def __unicode__(self):
        return self.stringify()

    def __call__(self, out):
        return self.serialize(out)

    def serialize(self, out):
        raise NotImplementedError('%s.serialize' % self.__class__.__name__)

    def stringify(self):
        from StringIO import StringIO
        out = StringIO()
        self.serialize(out)
        return out.getvalue()

    def substitute(self, out, name):
        value = self.env.get(name)

        if isinstance(value, Template):
            value.serialize(out)
        else:
            if value is None:
                value = ''
            elif callable(value):
                value = value()
            else:
                value = unicode(value)

            self.filter(value, self.out)

        return self
