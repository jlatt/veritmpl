#!/usr/bin/env python
# -*- coding: utf-8 -*-
import types


class Template(object):
    """Template is the base class for all veritmpl templates.
    In order to be treated as templates during the rendering process, an object
    must inherit from this class.

    """
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
            encoded = unicode(value)
            if value:
                out.write(encoded)
        return self

    def substitute(self, name, out):
        """Perform variable substitution in the template from the keyword
        arguments. Values are encoded before being written to the output
        stream.

        """
        value = self.env.get(name)
        self.substitute_value(value, out)
        return self

    def substitute_value(self, value, out):
        """Substitute a value into the template output stream.
        Templates and generators are recognized as special values.

        """
        if isinstance(value, Template):
            self.substitute_template(value, out)
        elif isinstance(value, types.GeneratorType):
            self.substitute_generator(value, out)
        else:
            self.encode(value, out)
        return self

    def substitute_template(self, template, out):
        """Write a template to the output stream."""
        template.__call__(out)
        return self

    def substitute_generator(self, generator, out):
        """Exhaust a generator. Write its values to the template output.

        """
        for value in generator:
            self.substitute_value(value, out)
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
