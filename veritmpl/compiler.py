import re


sub_regex = re.compile(r'(?<!\\){{\s*(?P<name>[_a-z]\w*)\s*}}', re.I | re.M)


def ensure_stream(out=None):
    """Return a file-like object. If the argument is None, it will be a
    StringIO instance.

    """
    if out is None:
        import StringIO
        out = StringIO.StringIO()
    return out


def compile_module(names=None, out=None, base=None, imports=None):
    """Compile a mapping from class names to token sequences into a module.
    The function accepts an optional base template for all classes and an
    optional sequence of imports.

    """
    imports = imports or ('import veritmpl.runtime',)
    out = ensure_stream(out)
    if imports:
        for imp in imports:
            print >>out, 'import %s' % imp
    for name, tokens in names.iteritems():
        print >>out
        print >>out
        compile_template(name, tokens, out, base)
    return out


def compile_template(name, tokens, out=None, base='veritmpl.runtime.Template'):
    """Compile a name and token sequence into a class declaration."""
    out = ensure_stream(out)

    print >>out, 'class %s(%s):' % (name, base)
    print >>out, '\tdef __call__(self, out):'
    for token_type, value in tokens:
        if token_type == 'literal':
            print >>out, '\t\tout.write(%r)' % value
        elif token_type == 'sub':
            print >>out, '\t\tself.substitute(%r, out)' % value
    print >>out, '\t\treturn out'

    return out


def parse(data):
    """Parse a string into a Template."""
    position = 0
    for match in sub_regex.finditer(data):
        if match.start() > position:
            yield ('literal', data[position:match.start()])
        yield ('sub', match.group('name'))
        position = match.end()

    if position < len(data) - 1:
        yield ('literal', data[position:])


if __name__ == '__main__':
    import optparse
    import os
    import sys


    optparser = optparse.OptionParser()
    optparser.add_option('-t', '--template', dest='template', help='Use a specific template class.', default=None)
    optparser.add_option('-i', '--import', dest='imports', action='append')
    (options, args) = optparser.parse_args()

    def gen_tokens():
        for fname in args:
            class_name = os.path.basename(fname).rsplit('.', 1)[0].capitalize()
            data = open(fname).read()
            tokens = parse(data)
            yield (class_name, tokens)
    classes = dict(gen_tokens())
    compile_module(names=classes, out=sys.stdout, base=options.template, imports=options.imports)
