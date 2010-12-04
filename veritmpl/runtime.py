class Template(object):
    """Template is the base class for all veritmpl templates.
    In order to be treated as templates during the rendering process, an object
    must inherit from this class.

    """
    EXHAUST_BYTES = 1024 * 1024

    output_encode = unicode

    expected_kwargs = tuple()

    def __init__(self, **kwargs):
        """Instantiate a template. Keyword arguments are used in rendering the
        template.

        """
        self.env = kwargs

    def __repr__(self):
        return '%s(**%r)' % (self.__class__.__name__, self.env)

    def __str__(self):
        """Stringify a template."""
        return self.stringify().encode('utf-8')

    def __unicode__(self):
        """Render a template to a string."""
        from StringIO import StringIO
        out = StringIO()
        self.__call__(out)
        return out.getvalue()

    def __call__(self, out):
        """Render a template to an output stream.
        This method must be implemented in base classes. Usually, it is
        implemented by compiler-generated classes.

        """
        raise NotImplementedError('%s.__call__' % self.__class__.__name__)

    def encode(self, value, out):
        """Write a python object to the output stream."""
        if value is not None:
            encoded = self.output_encode(value)
            if value:
                out.write(encoded)

    def substitute(self, name, out):
        """Perform variable substitution in the template from the keyword
        arguments. Values are encoded before being written to the output
        stream.

        """
        value = self.env.get(name)

        if isinstance(value, Template):
            value.__call__(out)
        elif hasattr(value, 'read') and callable(value.read): # TODO better file test?
            self.encode(value.read(), out)
        else:
            self.encode(value, out)

        return self


class Literal(unicode):
    """Literal is a base class for typed strings. It is used to mark certain
    strings as the output from an encoding process. These strings are usually
    recognized and passed verbatim by the encoding step during template
    rendering.

    """
    def __new__(cls, s=u'', *args, **kwargs):
        if isinstance(s, cls):
            return s
        else:
            return super(Literal, cls).__new__(cls, s, *args, **kwargs)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, unicode(self))
