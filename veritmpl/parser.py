import re


sub_regex = re.compile(r'(?<!\\){{\s*(?P<name>[_a-z]\w*)\s*}}', re.I | re.M)


def compile_template(name, tokens, out=None):
    if out is None:
        import StringIO
        out = StringIO.StringIO()

    print >>out, 'class %s(runtime.Template):' % name
    print >>out, '\tdef serialize(self, out):'
    for token_type, value in tokens:
        if token_type == 'literal':
            print >>out, '\t\tout.write(%r)' % value
        elif token_type == 'sub':
            print >>out, '\t\tself.substitute(out, %r)' % value
    print >>out, '\t\treturn out'

    return out


def parse(data):
    position = 0
    for match in sub_regex.finditer(data):
        if match.start() > position:
            yield ('literal', data[position:match.start()])
        yield ('sub', match.group('name'))
        position = match.end()

    if position < len(data) - 1:
        yield ('literal', data[position:])


if __name__ == '__main__':
    import sys


    data = sys.stdin.read()
    tokens = parse(data)
    output = compile_template(sys.argv[1], tokens)
    print output.getvalue()
