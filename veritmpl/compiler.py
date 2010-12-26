#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


__author__ = 'Jeremy Latt <jeremy.latt@gmail.com>'
__all__ = ('compile_module', 'compile_template', 'parse')


sub_regex = re.compile(r'(?<!\\){{\s*(?P<name>[_a-z]\w*)\s*}}', re.I | re.M)


def ensure_stream(out=None):
    """Return a file-like object. If the argument is None, it will be a
    StringIO instance.

    """
    if out is None:
        import StringIO
        out = StringIO.StringIO()
    return out


def compile_module(classes=None, out=None):
    """Compile a mapping from class names to token sequences into a module.
    The function accepts an optional base template for all classes and an
    optional sequence of imports.

    """
    out = ensure_stream(out)
    for kwargs in classes:
        compile_template(out=out, **kwargs)
        print >>out
        print >>out
    return out


template_types = dict(
    html='veritmpl.html.HTMLTemplate',
    js='veritmpl.json.JSONTemplate',
    json='veritmpl.json.JSONTemplate',
    )


def compile_template(class_name=None, tokens=None, template_type=None, out=None):
    """Compile a name and token sequence into a class declaration."""
    out = ensure_stream(out)
    base_class = template_types.get(template_type, 'veritmpl.runtime.Template')
    base_import, _ = base_class.rsplit('.', 1)
    expected_kwargs = set()
    print >>out, 'import %s' % base_import
    print >>out
    print >>out
    print >>out, 'class %s(%s):' % (class_name, base_class)
    print >>out, '\tdef __call__(self, out):'
    for token in tokens:
        if token['type'] == 'literal':
            print >>out, '\t\tout.write(%r)' % token['value']
        elif token['type'] == 'sub':
            print >>out, '\t\tself.substitute(%r, out)' % token['value']
            expected_kwargs.add(token['value'])
    print >>out, '\t\treturn out'
    print >>out
    print >>out, '\texpected_kwargs = %r' % (expected_kwargs,)

    return out


def parse(data):
    """Parse a string into a Template."""
    position = 0
    for match in sub_regex.finditer(data):
        if match.start() > position:
            yield dict(type='literal', value=data[position:match.start()])
        yield dict(type='sub', value=match.group('name'))
        position = match.end()

    if position < len(data) - 1:
        yield dict(type='literal', value=data[position:])


if __name__ == '__main__':
    import os
    import sys


    args = sys.argv[1:]
    def gen_classes():
        for fname in args:
            base, ext = os.path.basename(fname).rsplit('.', 1)
            class_name = base.capitalize()
            f = open(fname)
            data = f.read()
            tokens = parse(data)
            yield dict(class_name=class_name, template_type=ext, tokens=tokens)
    compile_module(classes=gen_classes(), out=sys.stdout)
